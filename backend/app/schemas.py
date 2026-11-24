from datetime import datetime
from pydantic import BaseModel, Field


class Source(BaseModel):
    document_id: str
    filename: str
    page: int | None = None
    excerpt: str
    score: float


class DocumentSummary(BaseModel):
    id: str
    filename: str
    content_type: str
    size_bytes: int
    chunks: int
    created_at: datetime


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[Source]


class HealthResponse(BaseModel):
    status: str
    service: str
