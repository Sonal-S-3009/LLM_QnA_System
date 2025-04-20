import pandas as pd

def parse_csv(file_path):
    """Extract data from CSV files."""
    try:
        df = pd.read_csv(file_path)
        text = df.to_string()
        return df, text if text.strip() else "No data found in CSV."
    except Exception as e:
        return None, f"CSV Extraction Error: {str(e)}"