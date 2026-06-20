from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.service import chat_service


def _find_frontend_dist() -> Path | None:
    candidates = [
        Path.cwd() / "frontend" / "dist",
        Path(__file__).resolve().parent / "frontend" / "dist",
        Path(__file__).resolve().parent.parent / "frontend" / "dist",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


FRONTEND_DIST = _find_frontend_dist()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class SourceItem(BaseModel):
    category: str
    question: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]


app = FastAPI(
    title="Helios Institution Student Support Chatbot API",
    description="RAG-powered Helios Institution FAQ assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/examples")
def examples() -> dict:
    return {"examples": chat_service.get_examples()}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = chat_service.ask(request.message)
        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if FRONTEND_DIST is not None:
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str) -> FileResponse:
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")


def main() -> None:
    import uvicorn

    print("Starting API server at http://127.0.0.1:8000")
    if FRONTEND_DIST is not None:
        print(f"Serving React frontend from {FRONTEND_DIST}")
    else:
        print("Frontend not built yet. Run: cd frontend && npm install && npm run build")
        print("Or start dev mode: cd frontend && npm run dev")

    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
