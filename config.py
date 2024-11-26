import os
from datetime import timedelta

class Config:
   
    SECRET_KEY = os.urandom(32)
    
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mohammed1@localhost:5432/student_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    
    
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)