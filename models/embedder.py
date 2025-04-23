from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from typing import List

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using SentenceTransformer."""
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query using SentenceTransformer."""
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embeddings = SentenceTransformerEmbeddings(model_name)

    def encode(self, texts):
        """Encode texts into embeddings (legacy method for VectorStore)."""
        return self.model.encode(texts, convert_to_numpy=True)

    def embedding_function(self):
        """Return LangChain-compatible Embeddings object."""
        return self.embeddings