import pytest
from models.qa_pipeline import index_documents, answer_query


def test_answer_query(tmp_path):
    file_path = tmp_path / "test.txt"
    with open(file_path, "w") as f:
        f.write("The capital of France is Paris.")

    index_documents([file_path])
    answer, refs = answer_query("What is the capital of France?")
    assert "Paris" in answer
    assert refs