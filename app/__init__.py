import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '../templates'),  # Templates path outside of app
                static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static'))  # Static files path (e.g., CSS, JS)
    
    app.config.from_object('config.Config')  # Load configuration settings from config.py
    CORS(app)  # Enable Cross-Origin Resource Sharing
    db.init_app(app)  # Initialize the database

    # Set file size limit in the app config
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16 MB
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../uploads')  # Path to the uploads folder

    # Import and register the blueprint for routes
    from .routes import routes
    app.register_blueprint(routes)

    # Create all database tables if needed
    with app.app_context():
        db.create_all()

    return app
