import logging
from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.rag import DbKnowledgeChunk
from app.services.rag.ingest import ingestion_engine
from app.services.rag.vector_db import vector_db

logger = logging.getLogger("app.services.rag.retrieve")

class RetrievalEngine:
    async def retrieve_contexts(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Compute query embedding, query vector db over candidate chunks, and return mapped items."""
        query_vector = ingestion_engine.generate_mock_embedding(query)
        
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbKnowledgeChunk))
            all_chunks = res.scalars().all()
            
            candidates = [
                {
                    "embedding": c.embedding_json.get("vector", []),
                    "content": c.content,
                    "metadata": c.metadata_json
                } for c in all_chunks
            ]
            
            results = vector_db.query_similarity(query_vector, candidates, top_k)
            return [
                {
                    "score": score,
                    "content": item["content"],
                    "metadata": item["metadata"]
                } for score, item in results
            ]

# Global retrieval engine instance
retrieval_engine = RetrievalEngine()
