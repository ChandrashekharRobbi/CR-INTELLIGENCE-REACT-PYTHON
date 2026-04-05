"""
FastAPI Backend — Serves RAG Pipeline + Section Data to React Frontend.
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from rag_pipeline import RAGPipeline
from config import PORTFOLIO_SECTIONS, DATA_FOLDER

# ---------- APP ----------
app = FastAPI(title="CR Intelligence API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- PIPELINE INIT ----------
groq_api_key = os.getenv("GROQ_API_KEY")
pipeline = None

if groq_api_key:
    pipeline = RAGPipeline(groq_api_key)
    pipeline.load_knowledge_base("data")
    print("Pipeline ready.")
else:
    print("WARNING: GROQ_API_KEY not set.")


# ---------- MODELS ----------
class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


class ChatResponse(BaseModel):
    query: str
    answer: str
    query_type: str = "general"
    context_chunks: int = 0
    status: str = "success"


# ---------- ENDPOINTS ----------
@app.get("/api/health")
def health():
    return {"status": "ok", "pipeline_ready": pipeline is not None}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")

    result = pipeline.query(req.query, top_k=req.top_k)
    return ChatResponse(
        query=result.get("query", req.query),
        answer=result.get("answer", "No response"),
        query_type=result.get("query_type", "general"),
        context_chunks=result.get("context_chunks", 0),
        status=result.get("status", "error"),
    )


@app.get("/api/sections/{section_name}")
def get_section(section_name: str):
    file_map = {
        "about": "about.txt",
        "experience": "experience.txt",
        "skills": "skills.txt",
        "education": "education.txt",
        "projects": "projects.txt",
        "achievements": "achievements.txt",
        "resume": "resume.txt",
        "contact": "contact.txt",
        "why_hire": "why_hire.txt",
    }

    if section_name not in file_map:
        raise HTTPException(status_code=404, detail=f"Section '{section_name}' not found")

    file_path = os.path.join(DATA_FOLDER, file_map[section_name])
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"section": section_name, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")


@app.get("/api/stats")
def get_stats():
    if not pipeline:
        return {"status": "not_ready"}
    return pipeline.get_index_stats()


# ---------- SERVE REACT BUILD (Production) ----------
frontend_build = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_build):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_build, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        return FileResponse(os.path.join(frontend_build, "index.html"))


# ---------- RUN ----------
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
