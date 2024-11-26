from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=50, message='Username must be between 4 and 50 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), 
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    class_name = StringField('Class', validators=[DataRequired()])
    total_marks = IntegerField('Total Marks', validators=[
        DataRequired(), 
        NumberRange(min=0, max=100, message='Marks must be between 0 and 100')
    ])
    image = FileField('Student Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Image only!')
    ])
    submit = SubmitField('Submit')