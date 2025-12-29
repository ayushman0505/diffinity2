from PyPDF2 import PdfReader
from docx import Document

def load_document(file):
    try:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            return " ".join(page.extract_text() or "" for page in reader.pages)

        elif file.name.endswith(".docx"):
            doc = Document(file)
            return " ".join(p.text for p in doc.paragraphs)

        else:
            return file.read().decode("utf-8")
    except Exception as e:
        return ""
