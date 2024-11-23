DataScanner - Document Scanning Web App
A simple web application built using Flask that allows users to upload and scan documents. The app integrates with Tesseract OCR to extract text from uploaded files (images, PDFs, and text files) and uses SQLAlchemy to store the processed data in a database.

Features

📂 Upload and Scan Documents
Upload files like images or PDFs for processing.

🖹 Text Extraction
Extract text from uploaded files using Tesseract OCR.

🏷️ Text Classification
Extracted text is categorized into types such as PIL, PHI, and PCI before storage.

💾 Database Storage
Scanned results are stored in a database for future access and management.

Technologies Used
Flask: Web framework for the application.
Tesseract OCR: Optical Character Recognition tool for extracting text.
SQLAlchemy: ORM used for database interactions.
Prerequisites

Make sure the following are installed on your system:

Python (version 3.6 or later)
pip (Python package manager)
Tesseract OCR

Install Tesseract
Windows: Download and install Tesseract.
macOS: Run brew install tesseract.
Ubuntu/Linux: Run sudo apt-get install tesseract-ocr.


Setup Instructions
1. Clone the Repository
Clone the repository to your local machine:
git clone https://github.com/nisargakunder/DataScanner
cd DataScanner

2. Install Python Dependencies
Install the required Python packages:
pip install -r requirements.txt

3. Configure Tesseract Path
If Tesseract is installed manually (e.g., on Windows), set its path in your project:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4. Set Up the Database
The database URI is defined in your app.py or configuration file. By default, it uses SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

6. Run the Application
Start the Flask app locally:
cd data_scanner
python app.py
The app will be accessible at http://127.0.0.1:5000.

Usage
Open the web app in your browser.
Navigate to the Upload page.
Choose a file (image, PDF, or text) to upload.
The app will scan the file and display the extracted text.
If enabled, the extracted text will be saved to the database.

