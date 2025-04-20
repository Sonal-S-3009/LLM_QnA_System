AI-Powered Document QA System
This project is a hackathon submission for an AI-powered General-Purpose Document Question Answering (QA) System. It handles multiple file formats, extracts content using OCR, crawls hyperlinks, and answers queries accurately using semantic search.
Features

Multi-Format Support: Upload and process PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT, PNG, JPG.
OCR Integration: Extract text from images and image-based PDFs using Tesseract.
Semantic Search: Use Sentence Transformers and FAISS for intelligent retrieval.
Accurate QA: Answers sourced only from uploaded content, no hallucinations.
Hyperlink Crawling: Fetch content from linked webpages.
Structured Data: Handle CSV, XLSX, JSON with pandas for data queries.
Bonus Features:
References: Show source files for answers.
Summarization: Generate document summaries.
Multiple File Support: Query across multiple uploaded files.


FastAPI Backend: Async API with interactive Swagger UI.
Frontend: Jinja2 templates with Tailwind CSS.

Setup

Clone the Repository:
git clone https://github.com/yourusername/llm_qna_app.git
cd llm_qna_app


Install Python 3.8+:

Download from python.org.


Install Tesseract OCR:

Ubuntu: sudo apt-get install tesseract-ocr
Windows: Download from Tesseract GitHub
macOS: brew install tesseract


Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Install Dependencies:
pip install -r requirements.txt


Run the Application:
./run.sh  # Linux/macOS
run.ps1   # Windows

Open http://localhost:8000 or http://localhost:8000/docs for Swagger UI.


Usage

Upload files via the web interface.
Ask questions or request a summary.
View answers with references to source files.

Directory Structure
llm_qna_app/
├── backend/
│   ├── api.py
│   └── config.py
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   └── results.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── uploads/
├── parsers/
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   └── pptx_parser.py
├── models/
│   ├── embedder.py
│   ├── retriever.py
│   └── qa_pipeline.py
├── utils/
│   └── file_utils.py
├── data/
├── tests/
│   ├── test_parsers.py
│   └── test_qa.py
├── .gitignore
├── requirements.txt
├── README.md
├── app.py
└── run.sh

Testing
pytest tests/

Contributing
Fork and submit pull requests. Report issues via GitHub.
License
MIT License
