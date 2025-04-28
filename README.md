Document Q&A System

A powerful web-based Q&A system that allows users to upload up to 10 documents (PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT, PNG, JPG, URLs), index their content, query information, summarize documents, and delete uploaded files. Built with FastAPI, LangChain, and the Google Gemini API, it supports large document handling, OCR, hyperlink crawling, and semantic caching for efficient performance.
Features

Multi-File Upload: Upload and index up to 10 documents at a time, supporting diverse formats (PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT, PNG, JPG, URLs).
Query System: Ask questions based on uploaded documents, with answers and references to source files.
Summarization: Generate concise summaries of all indexed documents.
Document Management: View uploaded documents with delete buttons for easy removal.
Large Document Support: Efficiently handle large documents using text chunking.
OCR and Image Support: Extract text from images (PNG, JPG) using Tesseract.
Hyperlink Crawling: Index content from URLs using web scraping.
Semantic Caching: Optimize query performance with LangChain’s caching.
User-Friendly Interface: Web interface built with HTML, CSS, and JavaScript for seamless interaction.
Error Handling: Robust logging and user feedback for uploads, queries, and deletions.

Technologies

Backend:

Python 3.9+: Core programming language.
FastAPI 0.103.1: High-performance web framework for API endpoints.
LangChain 0.3.3: Framework for LLM integration, document loading, and vector search.
langchain-google-genai 2.1.3: Integration with Google Gemini API.
langchain-community 0.3.3: Document loaders and vector stores.
langchain-text-splitters 0.3.0: Text chunking for large documents.


Google Gemini API (gemini-1.5-pro): LLM for query answering and summarization.
FAISS 1.7.4: Vector store for efficient similarity search.
Sentence Transformers (all-MiniLM-L6-v2): Embedding model for text indexing.
Unstructured 0.15.0: Universal document parser for multiple file types.
Tesseract OCR 0.3.10: Text extraction from images.
Other Libraries: pypdf, pdfplumber, docx2txt, openpyxl, pandas, beautifulsoup4, requests, pillow.


Frontend:

HTML/CSS/JavaScript: Responsive web interface with dynamic document display.
Jinja2 3.1.2: Templating for rendering the web page.


Deployment:

Uvicorn 0.23.2: ASGI server for running FastAPI.
dotenv 1.0.0: Environment variable management for API keys.



Methods

Document Loading:

Uses LangChain’s document loaders (PyPDFLoader, Docx2txtLoader, UnstructuredLoader, etc.) to extract text from various file formats.
Fallback to UnstructuredLoader for unsupported formats or parsing failures.
OCR with Tesseract for images and WebBaseLoader for URLs.


Text Indexing:

Embeds text using sentence-transformers/all-MiniLM-L6-v2.
Stores embeddings in FAISS for fast similarity search.
Chunks large documents with RecursiveCharacterTextSplitter (chunk size: 1000, overlap: 200) to handle memory constraints.


Query Processing:

Uses LLMChain with Gemini API for query answering.
Retrieves top-3 relevant document chunks via FAISS similarity_search.
Combines retrieved content as context for the LLM prompt.


Summarization:

Concatenates all document texts and generates a summary using Gemini API.
Optimized with a custom prompt template for concise output.


Document Management:

Tracks up to 10 documents with metadata (filename).
Supports deletion by rebuilding the FAISS vector store without the deleted document.


Optimizations:

Semantic Caching: Caches LLM responses with InMemoryCache for faster repeated queries.
Prompt Engineering: Custom prompts ensure accurate and concise responses.
Error Handling: Comprehensive logging and user-friendly error messages.



Prerequisites

Python 3.9+: Install from python.org.
Tesseract OCR: Install on Windows:
Download from Tesseract at UB Mannheim.
Add to PATH or set in backend/api.py:pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'




Google Gemini API Key:
Obtain from Google AI Studio.
Store in .env file (see Setup).


System Dependencies (Windows):
Microsoft Visual C++ Redistributable.
Rust (for some Python packages): Install via rustup.



Setup

Clone the Repository:
git clone https://github.com/Sonal-S-3009/LLM_QnA_System.git
cd llm_qna_app


Create and Activate Virtual Environment:
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac


Install Dependencies:
pip install --force-reinstall -r requirements.txt
pip install "unstructured[all-docs]"


Configure Environment:

Create a .env file in the root directory:echo GOOGLE_API_KEY=your_gemini_api_key_here > .env


Replace your_gemini_api_key_here with your Google Gemini API key.


Verify Tesseract (Windows):
tesseract --version



Usage

Run the Application:
python app.py


The server starts at http://localhost:8000.
Output:INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)




Access the Web Interface:

Open http://localhost:8000 in a browser.
Interface includes:
Upload Section: Upload up to 10 documents.
Document List: Shows uploaded filenames with delete buttons.
Query Section: Enter questions about document content.
Summarization Section: Generate summaries of all documents.




Upload Documents:

Select files (PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT, PNG, JPG, or enter URLs).
Click “Upload”.
See confirmation in the response area and updated document list (e.g., “Uploaded and indexed 3 files”).
Maximum 10 documents; excess uploads are rejected.


Query Documents:

Enter a query (e.g., “What is the capital of France?”).
Click “Submit Query”.
View the answer and referenced filenames (e.g., “Answer: Paris, References: test.pdf”).


Summarize Documents:

Click “Summarize”.
View a concise summary of all indexed documents.


Delete Documents:

Click “Delete” next to a document in the list.
See confirmation (e.g., “Deleted document: test.pdf”) and updated list.


Handle Large Documents:

Upload large files (e.g., 10MB+ PDFs or text files).
The system chunks content for efficient indexing and querying.



Example Workflow

Upload Files:

Upload test1.pdf (“The capital of France is Paris”), test2.docx (“The capital of Japan is Tokyo”), and test3.txt (“The capital of Brazil is Brasília”).
Document list shows: test1.pdf, test2.docx, test3.txt (count: 3/10).


Query:

Query: “List the capitals mentioned.”
Response: “The capitals mentioned are Paris, Tokyo, and Brasília.” with references to all three files.


Summarize:

Click “Summarize”.
Response: “The documents mention the capitals of France (Paris), Japan (Tokyo), and Brazil (Brasília).”


Delete:

Delete test1.pdf.
Document list updates to: test2.docx, test3.txt (count: 2/10).


Query Again:

Query: “What is the capital of France?”
Response: “No relevant information found in the documents.”



Project Structure
llm_qna_app/
├── backend/
│   ├── api.py              # FastAPI endpoints for upload, query, summarize, delete
│   ├── config.py           # Configuration (e.g., upload directory)
├── frontend/
│   ├── static/
│   │   ├── uploads/        # Temporary storage for uploaded files
│   ├── templates/
│   │   ├── index.html      # Web interface
├── models/
│   ├── embedder.py         # Text embedding with Sentence Transformers
│   ├── qa_pipeline.py      # Core logic for indexing, querying, summarization, deletion
│   ├── vector_store.py     # FAISS vector store setup
├── tests/                  # Test cases (if any)
├── .env                    # Environment variables (API key)
├── .gitignore              # Git ignore file
├── app.py                  # Main FastAPI application
├── requirements.txt        # Python dependencies
└── README.md               # This file

Troubleshooting

Upload Errors:

“Cannot upload files. Maximum 10 documents”: Ensure total documents (current + new) ≤ 10.
“No valid documents extracted”: Check file content (e.g., empty files or unsupported formats).
Logs: Check logs in console or enable file logging.


Query Errors:

“Error answering query”: Verify documents contain relevant content.
Test: Use test_query.py to isolate issues.


Large Document Issues:

Memory errors: Reduce chunk_size in qa_pipeline.py (e.g., to 500).
Timeouts: Increase Uvicorn timeout:uvicorn app:app --timeout-keep-alive 300




Gemini API Issues:

401 Unauthorized: Check GOOGLE_API_KEY in .env.
429 Rate Limit: Reduce max_tokens in qa_pipeline.py (e.g., to 500).
Test:python -c "from langchain_google_genai import ChatGoogleGenerativeAI; llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro', google_api_key='your_key'); print(llm.invoke('Test').content)"




Tesseract Errors (Windows):

Ensure Tesseract is installed and path is set in api.py.
Verify: tesseract --version.


Clear PyCharm Cache:

In PyCharm: File > Invalidate Caches / Restart.



Contributing

Fork the repository.
Create a feature branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push to branch: git push origin feature/your-feature.
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, open an issue or contact mailbox.sonal30@gmail.com.

Built with ❤️ using AI and open-source tools. Happy querying!
