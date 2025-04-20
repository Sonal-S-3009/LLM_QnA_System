import os
import re
import requests
from bs4 import BeautifulSoup
from backend.config import ALLOWED_EXTENSIONS
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from parsers.pptx_parser import parse_pptx
from parsers.xlsx_parser import parse_xlsx
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.txt_parser import parse_txt
from parsers.image_parser import parse_image


def crawl_url(url):
    """Crawl content from a URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        return text if text.strip() else "No content found on page."
    except Exception as e:
        return f"Web Crawling Error: {str(e)}"


def extract_hyperlinks(text):
    """Extract URLs from text."""
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    return url_pattern.findall(text)


def process_file(file_path):
    """Process a single file and extract content."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return f"Unsupported file format: {ext}", None, os.path.basename(file_path)

    text = ""
    df = None
    filename = os.path.basename(file_path)

    if ext == '.pdf':
        text = parse_pdf(file_path)
    elif ext == '.docx':
        text = parse_docx(file_path)
    elif ext == '.pptx':
        text = parse_pptx(file_path)
    elif ext == '.xlsx':
        df, text = parse_xlsx(file_path)
    elif ext == '.csv':
        df, text = parse_csv(file_path)
    elif ext == '.json':
        df, text = parse_json(file_path)
    elif ext == '.txt':
        text = parse_txt(file_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        text = parse_image(file_path)

    if text and "Error" not in text:
        urls = extract_hyperlinks(text)
        for url in urls:
            crawled_text = crawl_url(url)
            text += f"\n\nContent from {url}:\n{crawled_text}"

    return text, df, filename