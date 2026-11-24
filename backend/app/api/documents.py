from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import get_settings
from ..rag.ingestion import extract_chunks
from ..rag.store import InMemoryDocumentStore
from ..schemas import DocumentSummary

router = APIRouter(prefix="/api/documents", tags=["documents"])
store = InMemoryDocumentStore()


@router.post("/upload", response_model=DocumentSummary, status_code=201)
async def upload_document(file: UploadFile = File(...)) -> DocumentSummary:
    settings = get_settings()
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds the {settings.max_upload_mb} MB limit.")
    try:
        chunks = extract_chunks(file.filename or "upload", content)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    if not chunks:
        raise HTTPException(400, "The document contains no readable text.")
    document = store.add(file.filename or "upload", file.content_type or "application/octet-stream", len(content), chunks)
    return DocumentSummary(id=document.id, filename=document.filename, content_type=document.content_type, size_bytes=document.size_bytes, chunks=len(document.chunks), created_at=document.created_at)


@router.get("", response_model=list[DocumentSummary])
async def list_documents() -> list[DocumentSummary]:
    return [DocumentSummary(id=d.id, filename=d.filename, content_type=d.content_type, size_bytes=d.size_bytes, chunks=len(d.chunks), created_at=d.created_at) for d in store.documents.values()]


@router.delete("/{document_id}", status_code=204)
async def delete_document(document_id: str) -> None:
    if not store.delete(document_id):
        raise HTTPException(404, "Document not found.")
