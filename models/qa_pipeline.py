import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class QAPipeline:
    def __init__(self):
        self.documents = []  # List of dicts: {"text": str, "filename": str}
        self.uploaded_filenames = []
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def index_documents(self, texts, filenames):
        """Index documents with deduplication by filename."""
        logging.debug(f"Indexing {len(texts)} documents with filenames: {filenames}")
        indexed_docs = []
        for text, filename in zip(texts, filenames):
            if filename not in self.uploaded_filenames:
                chunks = self.text_splitter.split_text(text)
                for chunk in chunks:
                    doc = {"text": chunk, "filename": filename}
                    indexed_docs.append(doc)
                self.uploaded_filenames.append(filename)
        self.documents.extend(indexed_docs)
        self.rebuild_vector_store()
        logging.debug(f"Indexed {len(self.uploaded_filenames)} unique filenames: {self.uploaded_filenames}")

    def rebuild_vector_store(self):
        """Rebuild the FAISS vector store."""
        if self.documents:
            langchain_docs = [
                Document(page_content=doc["text"], metadata={"filename": doc["filename"]})
                for doc in self.documents
            ]
            self.vector_store = FAISS.from_documents(langchain_docs, self.embeddings)
        else:
            self.vector_store = None
        logging.debug(f"Vector store rebuilt with {len(self.documents)} documents")

    def answer_query(self, query):
        """Answer a query based on indexed documents."""
        if not self.vector_store:
            return "No documents indexed.", []
        docs = self.vector_store.similarity_search(query, k=5)  # Increased from 3 to 5
        context = "\n".join([doc.page_content for doc in docs])
        response = self.llm.invoke(f"Answer based on this context:\n{context}\nQuery: {query}").content
        # Format response with line breaks
        response = response.replace("\n", "<br>")
        references = list(dict.fromkeys([doc.metadata.get("filename", "Unknown") for doc in docs]))  # Remove duplicates
        return response, references

    def summarize_documents(self):
        """Summarize all indexed documents."""
        if not self.documents:
            return "No documents to summarize."
        all_text = "\n".join([doc["text"] for doc in self.documents])
        summary = self.llm.invoke(f"Summarize this text:\n{all_text}").content
        return summary.replace("\n", "<br>")  # Format with line breaks

    def get_document_count(self):
        """Return the number of unique documents."""
        return len(self.uploaded_filenames)

    def get_uploaded_filenames(self):
        """Return the list of uploaded filenames."""
        return self.uploaded_filenames.copy()

    def delete_document(self, filename):
        """Delete a document by filename."""
        if filename in self.uploaded_filenames:
            try:
                self.documents = [doc for doc in self.documents if doc["filename"] != filename]
                self.uploaded_filenames.remove(filename)
                self.rebuild_vector_store()
                logging.debug(f"Successfully deleted {filename} from index")
                return True
            except Exception as e:
                logging.error(f"Error deleting {filename}: {str(e)}")
                return False
        logging.warning(f"Filename {filename} not found for deletion")
        return False