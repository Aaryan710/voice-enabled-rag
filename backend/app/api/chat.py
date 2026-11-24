from uuid import uuid4
from fastapi import APIRouter

from ..config import get_settings
from ..rag.generation import compose_answer
from ..rag.retrieval import retrieve
from ..schemas import ChatRequest, ChatResponse, Source
from .documents import store

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    matches = retrieve(store, request.question, get_settings().top_k)
    sources = [Source(document_id=c.document_id, filename=c.filename, page=c.page, excerpt=c.text[:240], score=round(score, 3)) for c, score in matches]
    return ChatResponse(answer=compose_answer(request.question, matches), session_id=request.session_id or uuid4().hex, sources=sources)
