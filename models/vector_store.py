import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension=384):
        """Initialize FAISS index with dimension from sentence-transformers."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embeddings, documents):
        """Add embeddings and documents to the vector store."""
        embeddings = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding, k=3):
        """Search for top-k similar documents."""
        query_embedding = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_embedding, k)
        top_k_docs = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        scores = [float(dist) for dist in distances[0]]
        return top_k_docs, scores