import pptx

def parse_pptx(file_path):
    """Extract text from PPTX files."""
    try:
        prs = pptx.Presentation(file_path)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text if text.strip() else "No text found in PPTX."
    except Exception as e:
        return f"PPTX Extraction Error: {str(e)}"
