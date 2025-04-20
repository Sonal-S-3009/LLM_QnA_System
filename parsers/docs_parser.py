import docx

def parse_docx(file_path):
    """Extract text from DOCX files."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else "No text found in DOCX."
    except Exception as e:
        return f"DOCX Extraction Error: {str(e)}"