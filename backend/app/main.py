from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import chat, documents
from .config import get_settings
from .schemas import HealthResponse

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", description="Voice-first document intelligence API")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)
