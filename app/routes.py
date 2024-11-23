from flask import Blueprint, app, flash, jsonify, request, render_template
import os
from app.scanner import scan_file
from app.models import Scan  # Import scan_file function from scanner.py
from app import db
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
        
        # Render the results page and pass the extracted data
        return render_template('results.html', results=results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 # Ensure db is initialized correctly with the app
@routes.route('/view-all-results')
def view_all_results():
    # Fetch all results from the database
    results = Scan.query.all()
    
    # Render the results in the view-all-results.html template
    return render_template('view_all_results.html', results=results)
@routes.route('/delete/<int:id>', methods=['GET'])
def delete_result(id):
    result = Scan.query.get(id)
    if result:
        db.session.delete(result)
        db.session.commit()
        flash('Record deleted successfully!', 'success')
    else:
        flash('Record not found!', 'error')
    return render_template('view_all_results.html')