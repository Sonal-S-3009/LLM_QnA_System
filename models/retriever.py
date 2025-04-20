import faiss
import numpy as np


class Retriever:
    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.embeddings = []

    def add_documents(self, embeddings, documents):
        """Add documents and their embeddings to the index."""
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        if embeddings:
            self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query_embedding, k=3):
        """Search for top-k relevant documents."""
        if not self.embeddings:
            return [], []
        D, I = self.index.search(np.array([query_embedding]), k)
        return [(self.documents[i].text, self.documents[i].metadata["filename"]) for i in I[0] if i >= 0]