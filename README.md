# VoxKnowledge

Modular voice-first RAG foundation. The current runnable slice supports PDF, TXT, Markdown, and DOCX uploads, local retrieval, cited chat responses, and a React interface.

## Run (PowerShell)

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`; API docs are at `http://localhost:8000/docs`.

The retriever is intentionally local and provider-independent. The service boundaries are ready for FAISS/pgvector, Groq, Whisper, and TTS integrations in later phases.
