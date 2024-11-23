import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import os
import re
from datetime import datetime
from app import db  # Importing the db object from the app
from app.models import Scan # Importing the ScanResult model from models

# Set the Tesseract path if it's not in your system's PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# If Poppler is not installed globally, set the path to the Poppler bin folder
poppler_path = r'C:\Users\HP\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'

# Preprocess the image (convert to grayscale, apply sharpness, thresholding, etc.)
def preprocess_image(image_path):
    image = Image.open(image_path)
    
    # Convert the image to grayscale
    image = image.convert('L')
    
    # Enhance the image (increase sharpness)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    
    # Apply thresholding (converts the image to pure black and white)
    image = image.point(lambda p: p > 180 and 255)
    
    # Optional: Apply image filtering (e.g., remove noise)
    image = image.filter(ImageFilter.MedianFilter(3))
    
    return image

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    try:
        images = convert_from_path(file_path, poppler_path=poppler_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

# Function to extract text from an image
def extract_text_from_image(file_path):
    try:
        processed_image = preprocess_image(file_path)
        text = pytesseract.image_to_string(processed_image)
        return text
    except Exception as e:
        return {"error": f"Failed to extract text from image: {str(e)}"}

# Function to insert the scan result into the database
def insert_scan_result(card_type, card_number):
    result = Scan(
        card_type=card_type, 
        card_number=card_number, 
        timestamp=datetime.utcnow()
    )
    db.session.add(result)
    db.session.commit()

# Function to process the scan data and insert it into the database
def process_scan(scan_data):
    try:
        # Extract the card type and card number from the scan data
        card_type = scan_data.get("type")
        card_number = scan_data.get("matches")[0]  # Assuming the first match is the card number

        # Insert the result into the database
        insert_scan_result(card_type, card_number)

        return {"message": "Scan result successfully saved"}
    
    except Exception as e:
        return {"error": str(e)}

# Main function to scan and process the file
def scan_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
        if isinstance(text, dict) and "error" in text:
            return text
    elif ext in ['.txt', '.csv']:
        with open(file_path, 'r') as file:
            text = file.read()
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        text = extract_text_from_image(file_path)
        if isinstance(text, dict) and "error" in text:
            return text
    else:
        return {"error": "Unsupported file format"}

    print("Extracted Text: ", text)

    # Define the patterns for different card types
    patterns = {
        "PAN Card": r'[A-Z]{5}[0-9]{4}[A-Z]{1}',  # PAN card pattern
        "SSN": r'\d{3}-\d{2}-\d{4}',  # SSN pattern
        "Credit Card": r'(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})',  # Credit card pattern
        "Medical Record Number": r'(?:MNR[:\s]?\d{5,7})',  # Medical record pattern
        "Health Insurance": r'\d{9}-\d{1}',  # Health insurance pattern
    }

    results = []
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results.append({"type": label, "matches": matches})

    # If matches are found, insert them into the database
    for result in results:
        process_scan(result)

    return results  # Return the matches for further use

