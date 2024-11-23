from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Directly configure app settings (without using a separate config.py)
    app.config['SECRET_KEY'] = os.urandom(24)  # Use a random secret key for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy modification tracking
    
    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints (if any)
    from .routes import routes  # Assuming you have a blueprint for routes
    app.register_blueprint(routes)

    return app
