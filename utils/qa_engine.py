from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import re
from llama_index.core import Document

# Initialize Sentence Transformer and FAISS
model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)

# Global storage
documents = []
embeddings = []
dataframes = []


def index_documents(file_paths):
    """Index documents and their embeddings."""
    global documents, embeddings, faiss_index, dataframes
    from utils.file_processor import process_file

    documents = []
    embeddings = []
    dataframes = []
    faiss_index = faiss.IndexFlatL2(dimension)

    for file_path in file_paths:
        text, df, filename = process_file(file_path)
        if "Error" not in text:
            doc = Document(text=text, metadata={"filename": filename})
            documents.append(doc)
            dataframes.append((df, filename))
            embedding = model.encode(text, convert_to_numpy=True)
            embeddings.append(embedding)

    if embeddings:
        embeddings = np.array(embeddings).astype('float32')
        faiss_index.add(embeddings)


def answer_query(query):
    """Answer a query with references."""
    if not documents:
        return "No documents uploaded.", []

    query_lower = query.lower()
    if any(word in query_lower for word in ['sum', 'average', 'total', 'filter']):
        for df, filename in dataframes:
            if df is not None:
                try:
                    if 'sum' in query_lower:
                        column = re.search(r'sum of (\w+)', query_lower)
                        if column:
                            column = column.group(1)
                            if column in df.columns:
                                return f"Sum of {column}: {df[column].sum()}", [f"Data from {filename}"]
                    elif 'average' in query_lower:
                        column = re.search(r'average of (\w+)', query_lower)
                        if column:
                            column = column.group(1)
                            if column in df.columns:
                                return f"Average of {column}: {df[column].mean()}", [f"Data from {filename}"]
                    elif 'filter' in query_lower:
                        match = re.search(r'filter (\w+) where (\w+) > (\d+)', query_lower)
                        if match:
                            column, condition_col, value = match.groups()
                            if condition_col in df.columns:
                                result = df[df[condition_col] > int(value)][column]
                                return result.to_string(), [f"Data from {filename}"]
                except Exception as e:
                    return f"Data Query Error: {str(e)}", []

    query_embedding = model.encode(query, convert_to_numpy=True).astype('float32')
    D, I = faiss_index.search(np.array([query_embedding]), k=3)

    relevant_docs = [(documents[i].text, documents[i].metadata["filename"]) for i in I[0] if i >= 0]
    if not relevant_docs:
        return "Information not available in uploaded documents.", []

    context = "\n".join([doc[0] for doc in relevant_docs])
    references = [doc[1] for doc in relevant_docs]

    if query_lower.startswith("summarize"):
        words = context.split()[:100]
        return " ".join(words) + "...", references
    elif query_lower.startswith("what is"):
        sentences = context.split('.')
        for sentence in sentences:
            if query_lower[7:].strip() in sentence.lower():
                return sentence.strip() + ".", references
        return "Information not available.", references
    else:
        return relevant_docs[0][0][:500] + "..." if len(relevant_docs[0][0]) > 500 else relevant_docs[0][0], references


def summarize_documents():
    """Summarize all documents."""
    if not documents:
        return "No documents uploaded."

    all_text = "\n".join([doc.text for doc in documents])
    words = all_text.split()[:200]  # Basic summary: first 200 words
    return " ".join(words) + "..."