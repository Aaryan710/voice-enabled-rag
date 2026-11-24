from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class Chunk:
    document_id: str
    filename: str
    text: str
    page: int | None = None


@dataclass
class Document:
    id: str
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime
    chunks: list[Chunk]


class InMemoryDocumentStore:
    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}

    def add(self, filename: str, content_type: str, size_bytes: int, chunks: list[Chunk]) -> Document:
        document = Document(uuid4().hex, filename, content_type, size_bytes, datetime.now(timezone.utc), chunks)
        for chunk in chunks:
            chunk.document_id = document.id
        self.documents[document.id] = document
        return document

    def delete(self, document_id: str) -> bool:
        return self.documents.pop(document_id, None) is not None

    def all_chunks(self) -> list[Chunk]:
        return [chunk for document in self.documents.values() for chunk in document.chunks]
