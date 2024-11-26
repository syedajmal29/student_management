import os
from flask import Flask
from extensions import db, login_manager, bcrypt
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprint
    app.register_blueprint(main)

    # Ensure upload directory exists with absolute path
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    # Add a context processor to make current_user available in templates
    @app.context_processor
    def inject_current_user():
        from flask_login import current_user
        return dict(current_user=current_user)

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True)