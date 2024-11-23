DataScanner - Document Scanning Web App
A simple web application built using Flask that allows users to upload and scan documents. This app integrates with Tesseract OCR to extract text from uploaded images,pdf,text files and  uses SQLAlchemy to store processed data in a database.
Features:
Upload and scan document images.
Extract text from scanned images using Tesseract OCR.
Extracted Text is identified as PIL,PHI,PCI and stored in db
Store scanned results indatabase for future access and management.
Technologies Used
Flask: Web framework for building the application.
Tesseract OCR: Optical Character Recognition to extract text from images.
SQLAlchemy: ORM for database interaction.
Prerequisites
Before setting up the project, make sure you have the following installed on your machine:

Python (version 3.6 or later)
pip (Python package manager)
Tesseract (installed locally or via package manager)
Install Tesseract
For Windows: Tesseract Installer
For macOS: brew install tesseract
For Linux (Ubuntu): sudo apt-get install tesseract-ocr
Install Python Dependencies
Clone the repository to your local machine and install the required Python packages by running the following commands:
git clone "https://github.com/nisargakunder/DataScanner"
cd DataScanner
pip install -r requirements.txt
Setting Up the Application
1. Set up the database (if using SQLAlchemy)
If you're using SQLAlchemy to store scanned data, make sure your database is set up. You can configure the database in the app.py file by adjusting the database URI.
2. Configure Tesseract Path
If you installed Tesseract manually, make sure to specify the correct path in your project. For example:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
Running the Application Locally
You can run the Flask app locally using the following command:
cd data_scanner
python app.py
By default, the app will run at http://127.0.0.1:5000.
Usage
Navigate to the uploaded page of the app.
Choose a document file to upload (PDFs or images).
The document will be scanned, and the extracted text will be displayed on the page.
Optionally, save the results in your database if you’ve enabled that feature.
Directory Structure:
data_scanner/
├── app/                   # Application folder
│   ├── __init__.py        # Contains initialization logic
│   ├── models.py          #  database models
│   ├── routes.py          #  routes
│   ├── scanner.py         # Scanning logic
│   ├── templates/         # HTML templates
│   ├── instance/          # Database and config files (if any)
├── uploads/               # File uploads
├── app.py                 # Entry point of your application
├── requirements.txt       # Python dependencies
