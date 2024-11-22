import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///scanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
