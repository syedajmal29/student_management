import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models import User, Student
from forms import LoginForm, RegisterForm, StudentForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('main.register'))
        
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/student/create', methods=['GET', 'POST'])
@login_required
def create_student():
    form = StudentForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
        
        new_student = Student(
            name=form.name.data,
            class_name=form.class_name.data,
            total_marks=form.total_marks.data,
            image=image_filename
        )
        db.session.add(new_student)
        db.session.commit()
        
        flash('Student record created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('student_form.html', form=form, action='Create')

@main.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        student.name = form.name.data
        student.class_name = form.class_name.data
        student.total_marks = form.total_marks.data
        
        if form.image.data:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            student.image = image_filename
        
        db.session.commit()
        flash('Student record updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('student_form.html', form=form, student=student, action='Update')

@main.route('/student/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Optional: Delete associated images can
    if student.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], student.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(student)
    db.session.commit()
    
    flash('Student record deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))