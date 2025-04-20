from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def encode(self, text):
        """Generate embeddings for text."""
        return self.model.encode(text, convert_to_numpy=True).astype('float32')