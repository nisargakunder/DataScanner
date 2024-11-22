from flask import Blueprint, jsonify, request, render_template
import os
from app.scanner import scan_file  # Import scan_file function from scanner.py

# Create a blueprint for routes
routes = Blueprint('routes', __name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Handle the upload form (Main page)
@routes.route('/', methods=['GET'])
def index():
    return render_template('upload.html')  # Render the main page with the upload form

# Handle file upload route
@routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Scan the uploaded file
    try:
        results = scan_file(file_path)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
