import os
import logging
import pytesseract
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import List
import traceback
from models.qa_pipeline import QAPipeline
from backend.config import UPLOAD_DIR
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    CSVLoader,
    JSONLoader,
    TextLoader,
    UnstructuredImageLoader,
    WebBaseLoader,
)
from unstructured.partition.auto import partition  # Direct unstructured import

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

router = APIRouter()
qa_pipeline = QAPipeline()


async def parse_file(file: UploadFile):
    """Parse uploaded file based on its extension."""
    filename = file.filename
    file_ext = os.path.splitext(filename)[1].lower()
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file to disk
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        logging.error(f"Error saving file {filename}: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error saving file: {str(e)}"})

    logging.debug(f"Starting to parse file: {filename} with extension: {file_ext}")
    text = ""

    try:
        if file_ext == ".pdf":
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"PyPDFLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"PyPDFLoader failed for {filename}: {str(e)}")
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                logging.debug(f"pdfplumber extracted text from {filename}: {len(text)} characters")

        elif file_ext == ".docx":
            try:
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"Docx2txtLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"Docx2txtLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext == ".pptx":
            try:
                loader = UnstructuredPowerPointLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"UnstructuredPowerPointLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"UnstructuredPowerPointLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext in [".xlsx", ".xls"]:
            try:
                loader = UnstructuredExcelLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"UnstructuredExcelLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"UnstructuredExcelLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext == ".csv":
            try:
                loader = CSVLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"CSVLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"CSVLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext == ".json":
            try:
                loader = JSONLoader(file_path, jq_schema=".", text_content=False)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"JSONLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"JSONLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext == ".txt":
            try:
                loader = TextLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"TextLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"TextLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        elif file_ext in [".png", ".jpg", ".jpeg"]:
            try:
                loader = UnstructuredImageLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
                logging.debug(f"UnstructuredImageLoader extracted text from {filename}: {len(text)} characters")
            except Exception as e:
                logging.debug(f"UnstructuredImageLoader failed for {filename}: {str(e)}")
                elements = partition(filename=file_path)
                text = "\n".join([str(el) for el in elements])
                logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        else:
            elements = partition(filename=file_path)
            text = "\n".join([str(el) for el in elements])
            logging.debug(f"Unstructured partition extracted text from {filename}: {len(text)} characters")

        if not text.strip():
            logging.warning(f"No text extracted from {filename}")
            return None, None

        logging.debug(f"Finished parsing {filename} with {len(text)} characters")
        return text, filename

    finally:
        # Clean up file from disk
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.debug(f"Deleted temporary file: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting temporary file {file_path}: {str(e)}")


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and index multiple files."""
    texts = []
    filenames = []

    if not files:
        logging.error("No files uploaded")
        raise HTTPException(status_code=400, detail={"error": "No files uploaded"})

    if len(files) > 10:
        logging.error(f"Too many files uploaded: {len(files)}. Maximum is 10.")
        raise HTTPException(status_code=400, detail={"error": f"Too many files uploaded. Maximum is 10."})

    try:
        current_count = qa_pipeline.get_document_count()
        if current_count + len(files) > 10:
            logging.error(
                f"Upload would exceed maximum of 10 documents. Current: {current_count}, Attempted: {len(files)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Cannot upload {len(files)} files. Maximum 10 documents allowed (current: {current_count})."}
            )

        for file in files:
            text, filename = await parse_file(file)
            if text and filename:
                logging.debug(f"Adding {filename} to index with {len(text)} characters")
                texts.append(text)
                filenames.append(filename)

        if not texts:
            logging.error("No valid documents extracted from uploaded files")
            raise HTTPException(status_code=400, detail={"error": "No valid documents extracted"})

        qa_pipeline.index_documents(texts, filenames)
        uploaded_filenames = qa_pipeline.get_uploaded_filenames()
        logging.debug(f"Indexed {len(uploaded_filenames)} unique filenames: {uploaded_filenames}")
        return {
            "message": f"Uploaded and indexed {len(texts)} files",
            "filenames": uploaded_filenames,
            "document_count": qa_pipeline.get_document_count()
        }

    except ValueError as ve:
        logging.error(f"Error uploading files: {str(ve)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail={"error": str(ve)})
    except Exception as e:
        logging.error(f"Error uploading files: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error uploading files: {str(e)}"})


@router.post("/query")
async def query(query: str = Form(...)):
    """Process a query."""
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
    """Summarize all indexed documents."""
    logging.debug("Processing summarization request")
    try:
        summary = qa_pipeline.summarize_documents()
        return {"summary": summary}
    except Exception as e:
        logging.error(f"Error processing summarization: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error processing summarization: {str(e)}"})


@router.post("/delete")
async def delete_document(filename: str = Form(...)):
    """Delete a document by filename."""
    logging.debug(f"Received delete request for: {filename}")
    if not filename.strip():
        logging.error("Empty filename received")
        raise HTTPException(status_code=400, detail={"error": "Filename cannot be empty"})
    try:
        success = qa_pipeline.delete_document(filename)
        if not success:
            logging.error(f"Failed to delete document: {filename}")
            raise HTTPException(status_code=500, detail={"error": f"Failed to delete document: {filename}"})
        uploaded_filenames = qa_pipeline.get_uploaded_filenames()
        logging.debug(f"Deleted document: {filename}. Remaining documents: {uploaded_filenames}")
        return {
            "message": f"Deleted document: {filename}",
            "filenames": uploaded_filenames,
            "document_count": qa_pipeline.get_document_count()
        }
    except Exception as e:
        logging.error(f"Error deleting document: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error deleting document: {str(e)}"})