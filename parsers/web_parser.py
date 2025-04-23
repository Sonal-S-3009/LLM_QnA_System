from bs4 import BeautifulSoup
import requests

def parse_web_content(file_path: str) -> str:
       """Parse text from an HTML file or URL."""
       try:
           if file_path.startswith(('http://', 'https://')):
               response = requests.get(file_path)
               response.raise_for_status()
               soup = BeautifulSoup(response.text, 'html.parser')
           else:
               with open(file_path, 'r', encoding='utf-8') as f:
                   soup = BeautifulSoup(f, 'html.parser')
           return soup.get_text(separator='\n', strip=True)
       except Exception as e:
           return f"Error parsing web content: {str(e)}"