from docx import Document

def parse_docx(file_path: str) -> str:
       """Parse text from a DOCX file."""
       try:
           doc = Document(file_path)
           text = [para.text for para in doc.paragraphs if para.text.strip()]
           return '\n'.join(text) if text else "No text extracted from DOCX."
       except Exception as e:
           return f"Error parsing DOCX: {str(e)}"