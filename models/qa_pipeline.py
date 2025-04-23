from models.embedder import Embedder
from models.vector_store import VectorStore
from llama_index import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.cache import InMemoryCache
import langchain
from dotenv import load_dotenv
import os
import logging
import warnings
import traceback

# Suppress huggingface_hub FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Enable semantic caching
langchain.llm_cache = InMemoryCache()

# Define prompt template
qa_prompt_template = """Use the following context to answer the query concisely and accurately. If the context doesn't contain relevant information, say so.
Context: {context}
Query: {query}
Answer:"""
qa_prompt = PromptTemplate(input_variables=["context", "query"], template=qa_prompt_template)

summary_prompt_template = """Summarize the following content concisely, capturing key points:
Content: {context}
Summary:"""
summary_prompt = PromptTemplate(input_variables=["context"], template=summary_prompt_template)

class QAPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.documents = []
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=api_key,
                temperature=0.7,
                max_tokens=500
            )
        except Exception as e:
            logging.error(f"Error initializing LLM: {str(e)}\n{traceback.format_exc()}")
            raise
        try:
            self.vectorstore = FAISS.from_texts([""], self.embedder.embedding_function())
        except Exception as e:
            logging.error(f"Error initializing FAISS: {str(e)}\n{traceback.format_exc()}")
            raise
        try:
            self.qa_chain = LLMChain(llm=self.llm, prompt=qa_prompt)
            logging.debug(f"LLMChain initialized with input_variables: {qa_prompt.input_variables}")
        except Exception as e:
            logging.error(f"Error initializing LLMChain: {str(e)}\n{traceback.format_exc()}")
            raise

    def index_documents(self, texts, filenames):
        """Index documents into the vector store."""
        logging.debug(f"Indexing {len(texts)} documents: {filenames}")
        self.documents = [Document(text=text, metadata={"filename": filename}) for text, filename in zip(texts, filenames)]
        try:
            self.vectorstore = FAISS.from_texts(
                texts,
                self.embedder.embedding_function(),
                metadatas=[{"filename": f} for f in filenames]
            )
        except Exception as e:
            logging.error(f"Error indexing documents: {str(e)}\n{traceback.format_exc()}")
            raise

    def answer_query(self, query):
        """Answer a query using manual retrieval and LLMChain."""
        logging.debug(f"Processing query: {query}")
        try:
            # Retrieve relevant documents
            docs = self.vectorstore.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            references = [
                {"filename": doc.metadata["filename"], "score": 1.0}
                for doc in docs
            ]
            logging.debug(f"Retrieved {len(docs)} documents for context: {len(context)} characters")
            # Run LLMChain with context and query
            input_dict = {"context": context, "query": query}
            logging.debug(f"Input to QA chain: {input_dict}")
            result = self.qa_chain.invoke(input_dict)
            logging.debug(f"QA chain result: {result}")
            answer = result["text"].strip()
            return answer, references
        except Exception as e:
            logging.error(f"Error in answer_query: {str(e)}\n{traceback.format_exc()}")
            return f"Error answering query: {str(e)}", []

    def summarize_documents(self):
        """Summarize all indexed documents."""
        if not self.documents:
            return "No documents to summarize."

        context = "\n".join([doc.text for doc in self.documents])
        logging.debug(f"Summarizing documents with context length: {len(context)}")
        try:
            response = self.llm.invoke(summary_prompt.format(context=context))
            summary = response.content.strip()
            return summary
        except Exception as e:
            logging.error(f"Error in summarize_documents: {str(e)}\n{traceback.format_exc()}")
            return f"Error summarizing documents: {str(e)}"