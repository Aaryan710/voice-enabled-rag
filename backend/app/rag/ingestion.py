from io import BytesIO
from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader

from .store import Chunk

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def extract_chunks(filename: str, content: bytes, chunk_size: int = 900, overlap: int = 120) -> list[Chunk]:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Supported files are PDF, TXT, Markdown, and DOCX.")
    if suffix == ".pdf":
        reader = PdfReader(BytesIO(content))
        page_texts = [(page.extract_text() or "", number) for number, page in enumerate(reader.pages, start=1)]
    elif suffix == ".docx":
        doc = DocxDocument(BytesIO(content))
        page_texts = [("\n".join(p.text for p in doc.paragraphs), None)]
    else:
        page_texts = [(content.decode("utf-8", errors="replace"), None)]
    chunks: list[Chunk] = []
    for text, page in page_texts:
        normalized = " ".join(text.split())
        if not normalized:
            continue
        start = 0
        while start < len(normalized):
            end = min(len(normalized), start + chunk_size)
            chunks.append(Chunk(document_id="", filename=filename, text=normalized[start:end], page=page))
            if end == len(normalized):
                break
            start = max(end - overlap, start + 1)
    return chunks
