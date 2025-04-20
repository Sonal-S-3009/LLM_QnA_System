import pdfplumber
from PIL import Image
import pytesseract

def parse_pdf(file_path):
    """Extract text from PDFs, including image-based ones."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    img = page.to_image().original
                    ocr_text = pytesseract.image_to_string(img)
                    text += ocr_text + "\n"
            return text if text.strip() else "No text found in PDF."
    except Exception as e:
        return f"PDF Extraction Error: {str(e)}"