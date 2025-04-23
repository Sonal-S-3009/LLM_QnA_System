import pdfplumber
import pytesseract
from PIL import Image
import io

def parse_pdf(file_path: str) -> str:
       """Parse text and images from a PDF file."""
       try:
           text = []
           with pdfplumber.open(file_path) as pdf:
               for page in pdf.pages:
                   # Extract text
                   page_text = page.extract_text()
                   if page_text:
                       text.append(page_text)
                   # Extract images for OCR
                   for img in page.images:
                       img_data = img['stream'].get_data()
                       image = Image.open(io.BytesIO(img_data))
                       ocr_text = pytesseract.image_to_string(image)
                       if ocr_text.strip():
                           text.append(ocr_text)
           return '\n'.join(text) if text else "No text extracted from PDF."
       except Exception as e:
           return f"Error parsing PDF: {str(e)}"