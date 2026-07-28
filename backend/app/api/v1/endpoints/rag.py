from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.rag.ingest import ingestion_engine
from app.services.rag.retrieve import retrieval_engine
from app.services.rag.context_builder import context_builder

router = APIRouter()

@router.post("/knowledge/upload", response_model=dict)
async def upload_document(
    title: str,
    content: str,
    doc_type: str = "markdown",
    user: Any = Depends(get_current_user)
) -> dict:
    doc = await ingestion_engine.ingest_document(
        owner_id=user.id,
        title=title,
        content=content,
        doc_type=doc_type
    )
    return {"status": "ingested", "document_id": str(doc.id), "title": doc.title}

@router.post("/knowledge/search", response_model=dict)
async def semantic_search(
    query: str,
    top_k: int = 3,
    user: Any = Depends(get_current_user)
) -> dict:
    chunks = await retrieval_engine.retrieve_contexts(query, top_k)
    context_str = context_builder.assemble_prompt_context(chunks)
    return {
        "query": query,
        "context": context_str,
        "results_count": len(chunks)
    }

from typing import Any
