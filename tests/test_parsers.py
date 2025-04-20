import pytest
import os
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from parsers.pptx_parser import parse_pptx
from parsers.xlsx_parser import parse_xlsx
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.txt_parser import parse_txt
from parsers.image_parser import parse_image
import pandas as pd
import json

def test_pdf_parser(tmp_path):
    # Note: Testing PDF requires a real file; assume test.pdf exists
    assert "Error" not in parse_pdf("tests/test_files/test.pdf")  # Replace with actual test file

def test_docx_parser(tmp_path):
    docx_path = tmp_path / "test.docx"
    from docx import Document
    doc = Document()
    doc.add_paragraph("Test content")
    doc.save(docx_path)
    assert parse_docx(docx_path) == "Test content"

def test_pptx_parser(tmp_path):
    # Note: Testing PPTX requires a real file; assume test.pptx exists
    assert "Error" not in parse_pptx("tests/test_files/test.pptx")  # Replace with actual test file

def test_xlsx_parser(tmp_path):
    xlsx_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_excel(xlsx_path, index=False)
    parsed_df, text = parse_xlsx(xlsx_path)
    assert parsed_df.equals(df)
    assert "1" in text

def test_csv_parser(tmp_path):
    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_csv(csv_path, index=False)
    parsed_df, text = parse_csv(csv_path)
    assert parsed_df.equals(df)
    assert "1" in text

def test_json_parser(tmp_path):
    json_path = tmp_path / "test.json"
    data = {"name": "Test", "value": 42}
    with open(json_path, 'w') as f:
        json.dump(data, f)
    parsed_df, text = parse_json(json_path)
    assert parsed_df["name"].iloc[0] == "Test"
    assert "Test" in text

def test_txt_parser(tmp_path):
    txt_path = tmp_path / "test.txt"
    with open(txt_path, 'w') as f:
        f.write("Test content")
    assert parse_txt(txt_path) == "Test content"

def test_image_parser(tmp_path):
    # Note: Testing image OCR requires a real image; assume test.png exists
    assert "Error" not in parse_image("tests/test_files/test.png")  # Replace with actual test image