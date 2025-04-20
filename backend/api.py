from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from typing import List
import os
from backend.config import UPLOAD_DIR
from models.qa_pipeline import index_documents, answer_query, summarize_documents

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload", response_class=HTMLResponse)
async def upload_files(request: Request, files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_paths = []

    for file in files:
        if file.filename:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            file_paths.append(file_path)

    if not file_paths:
        raise HTTPException(status_code=400, detail="No files uploaded")

    index_documents(file_paths)
    return templates.TemplateResponse("results.html", {"request": request})


@router.post("/query", response_class=HTMLResponse)
async def query(request: Request, query: str = Form(None), action: str = Form(...)):
    if action == "ask" and query:
        answer, references = answer_query(query)
        return templates.TemplateResponse("results.html",
                                          {"request": request, "answer": answer, "references": references})
    elif action == "summarize":
        summary = summarize_documents()
        return templates.TemplateResponse("results.html", {"request": request, "summary": summary})

    raise HTTPException(status_code=400, detail="Invalid action")