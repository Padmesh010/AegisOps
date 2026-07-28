import pytest
from app.services.rag.vector_db import vector_db
from app.services.rag.ingest import ingestion_engine
from app.services.rag.context_builder import context_builder

def test_cosine_similarity():
    vec_a = [1.0, 0.0, 0.0]
    vec_b = [1.0, 0.0, 0.0]
    sim = vector_db.cosine_similarity(vec_a, vec_b)
    assert sim == 1.0
    
    vec_c = [0.0, 1.0, 0.0]
    sim_ortho = vector_db.cosine_similarity(vec_a, vec_c)
    assert sim_ortho == 0.0

def test_chunking_overlaps():
    text = "AegisOps is an AI-powered platform for automated remediation."
    chunks = ingestion_engine.chunk_text(text, chunk_size=20, overlap=5)
    assert len(chunks) > 1

def test_context_budgeting_limits():
    chunks = [
        {"content": "First document chunk details", "metadata": {"chunk_index": 0}},
        {"content": "Second document chunk details", "metadata": {"chunk_index": 1}}
    ]
    context = context_builder.assemble_prompt_context(chunks, char_budget=80)
    assert "First" in context
    assert "Second" not in context  # exceeds budget
