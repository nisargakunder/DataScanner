import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import re
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
# Set the Tesseract path if it's not in your system's PATH
# Modify this line if necessary, based on where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# If Poppler is not installed globally, set the path to the Poppler bin folder
poppler_path = r'C:\Users\HP\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'
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
    
    # Return the processed image
    return image
def extract_text_from_pdf(file_path):
    try:
        images = convert_from_path(file_path, poppler_path=poppler_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

def extract_text_from_image(file_path):
    try:
        processed_image = preprocess_image(file_path)
        text = pytesseract.image_to_string(processed_image)
        return text
    except Exception as e:
        return {"error": f"Failed to extract text from image: {str(e)}"}

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
    patterns = {
        "PAN Card": r'[A-Z]{5}[0-9]{4}[A-Z]{1}', 
        "SSN": r'\d{3}-\d{2}-\d{4}',  
        "Credit Card": r'(\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})',  
        "Medical Record Number": r'(?:MNR[:\s]?\d{5,7})',  
        "Health Insurance": r'\d{9}-\d{1}',  
    }

    results = []
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results.append({"type": label, "matches": matches})

    return results
