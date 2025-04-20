from PIL import Image
import pytesseract

def parse_image(file_path):
    """Extract text from images using Tesseract OCR."""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "No text found in image."
    except Exception as e:
        return f"Image Extraction Error: {str(e)}"