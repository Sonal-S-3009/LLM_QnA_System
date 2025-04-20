import pandas as pd

def parse_xlsx(file_path):
    """Extract data from XLSX files."""
    try:
        df = pd.read_excel(file_path)
        text = df.to_string()
        return df, text if text.strip() else "No data found in XLSX."
    except Exception as e:
        return None, f"XLSX Extraction Error: {str(e)}"