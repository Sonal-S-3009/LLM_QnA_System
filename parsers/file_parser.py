import os
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .pptx_parser import parse_pptx
from .image_parser import parse_image
from .web_parser import parse_web_content
import pandas as pd
import json

def parse_file(file_path: str, filename: str) -> str:
    """Parse a file based on its extension and return its text content."""
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == '.pdf':
            return parse_pdf(file_path)
        elif ext == '.docx':
            return parse_docx(file_path)
        elif ext == '.pptx':
            return parse_pptx(file_path)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return parse_image(file_path)
        elif ext in ['.xlsx', '.csv']:
            df = pd.read_excel(file_path) if ext == '.xlsx' else pd.read_csv(file_path)
            return df.to_string()
        elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return json.dumps(data, indent=2)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext in ['.html', '.htm']:
            return parse_web_content(file_path)
        else:
            return "Unsupported file type."
    except Exception as e:
        return f"Error parsing {filename}: {str(e)}"