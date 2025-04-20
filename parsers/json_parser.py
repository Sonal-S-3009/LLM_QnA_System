import pandas as pd
import json

def parse_json(file_path):
    """Extract data from JSON files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        text = json.dumps(data, indent=2)
        return df, text if text.strip() else "No data found in JSON."
    except Exception as e:
        return None, f"JSON Extraction Error: {str(e)}"