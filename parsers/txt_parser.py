def parse_txt(file_path):
    """Extract text from TXT files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text if text.strip() else "No text found in TXT."
    except Exception as e:
        return f"TXT Extraction Error: {str(e)}"