import pytesseract
from PIL import Image

def parse_image(file_path: str) -> str:
       """Parse text from an image using OCR."""
       try:
           image = Image.open(file_path)
           text = pytesseract.image_to_string(image)
           return text if text.strip() else "No text extracted from image."
       except Exception as e:
           return f"Error parsing image: {str(e)}"