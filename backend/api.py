from fastapi import APIRouter, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.qa_pipeline import QAPipeline
import os
from backend.config import UPLOAD_DIR
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader, UnstructuredExcelLoader, CSVLoader, JSONLoader, TextLoader
from PIL import Image
import pytesseract
import logging
import io
import requests
from bs4 import BeautifulSoup
import pdfplumber
import traceback

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
qa_pipeline = QAPipeline()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(file_path):
    """Extract text from an image using OCR."""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        logging.error(f"Error in OCR for {file_path}: {str(e)}")
        return ""

def crawl_hyperlink(url):
    """Crawl a URL and extract text content."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3']))
        return text
    except Exception as e:
        logging.error(f"Error crawling {url}: {str(e)}")
        return ""

def parse_file(file_path, filename):
    """Parse various file types using LangChain loaders or pdfplumber for PDFs."""
    try:
        ext = os.path.splitext(filename)[1].lower()
        logging.debug(f"Parsing file: {filename} with extension: {ext}")
        if ext == '.pdf':
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                if not text.strip():
                    raise ValueError("PyPDFLoader extracted empty text")
                logging.debug(f"PyPDFLoader extracted text from {filename}: {len(text)} characters")
                return text
            except Exception as e:
                logging.error(f"PyPDFLoader failed for {filename}: {str(e)}")
                logging.debug(f"Falling back to pdfplumber for {filename}")
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                if not text.strip():
                    raise ValueError("pdfplumber extracted empty text")
                logging.debug(f"pdfplumber extracted text from {filename}: {len(text)} characters")
                return text
        elif ext == '.docx':
            loader = Docx2txtLoader(file_path)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext == '.pptx':
            loader = UnstructuredPowerPointLoader(file_path)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext in ['.xlsx', '.xls']:
            loader = UnstructuredExcelLoader(file_path)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext == '.csv':
            loader = CSVLoader(file_path)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext == '.json':
            loader = JSONLoader(file_path, jq_schema='.', text_content=False)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext == '.txt':
            loader = TextLoader(file_path)
            docs = loader.load()
            return "\n".join([doc.page_content for doc in docs])
        elif ext in ['.png', '.jpg', '.jpeg']:
            return extract_text_from_image(file_path)
        elif filename.startswith('http://') or filename.startswith('https://'):
            return crawl_hyperlink(filename)
        else:
            logging.warning(f"Unsupported file type: {ext}")
            return ""
    except Exception as e:
        logging.error(f"Error parsing {filename}: {str(e)}\n{traceback.format_exc()}")
        return ""

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    texts = []
    filenames = []
    errors = []
    for file in files:
        filename = file.filename
        logging.debug(f"Processing upload: {filename}")
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            content = await file.read()
            if not content:
                logging.error(f"Empty file uploaded: {filename}")
                errors.append(f"Empty file: {filename}")
                continue
            with open(file_path, "wb") as f:
                f.write(content)
            text = parse_file(file_path, filename)
            if text:
                texts.append(text)
                filenames.append(filename)
                logging.debug(f"Successfully processed {filename}: {len(text)} characters")
            else:
                logging.warning(f"No text extracted from {filename}")
                errors.append(f"No text extracted from {filename}")
        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}\n{traceback.format_exc()}")
            errors.append(f"Error processing {filename}: {str(e)}")
    if texts:
        try:
            qa_pipeline.index_documents(texts, filenames)
            return {"message": f"Uploaded and indexed {len(texts)} files", "errors": errors}
        except Exception as e:
            logging.error(f"Error indexing documents: {str(e)}\n{traceback.format_exc()}")
            return {"message": "Failed to index documents", "errors": errors + [f"Indexing error: {str(e)}"]}
    return {"message": "No valid files uploaded", "errors": errors}

@router.post("/query")
async def query(query: str = Form(...)):
    logging.debug(f"Received query: {query}")
    if not query.strip():
        logging.error("Empty query received")
        raise HTTPException(status_code=400, detail={"error": "Query cannot be empty"})
    logging.debug(f"Processing query: {query}")
    try:
        response, references = qa_pipeline.answer_query(query)
        return {"response": response, "references": references}
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error processing query: {str(e)}"})

@router.post("/summarize")
async def summarize():
    logging.debug("Processing summarization request")
    try:
        summary = qa_pipeline.summarize_documents()
        return {"summary": summary}
    except Exception as e:
        logging.error(f"Error summarizing documents: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error summarizing documents: {str(e)}"})