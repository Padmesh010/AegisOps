import uuid
import hashlib
from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.rag import DbKnowledgeDocument, DbKnowledgeChunk

class DocumentIngestionEngine:
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split document string contents using character chunk overlaps checks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
        return chunks

    def generate_mock_embedding(self, text: str, dimension: int = 1536) -> List[float]:
        """Generate deterministic float array using hash digests of string content."""
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # Scale bytes to float range [-1, 1]
        vals = []
        for i in range(min(dimension, len(h))):
            vals.append(float((h[i] - 127.5) / 127.5))
        # Zero-pad if dimension exceeds hash length
        if len(vals) < dimension:
            vals.extend([0.0] * (dimension - len(vals)))
        return vals

    async def ingest_document(
        self,
        owner_id: uuid.UUID,
        title: str,
        content: str,
        doc_type: str
    ) -> DbKnowledgeDocument:
        """Parse contents, generate chunks and embeddings, and persist models records."""
        async with TestingSessionLocal() as session:
            doc = DbKnowledgeDocument(
                title=title,
                content=content,
                doc_type=doc_type,
                owner_id=owner_id
            )
            session.add(doc)
            await session.flush()
            
            raw_chunks = self.chunk_text(content)
            for idx, raw_chunk in enumerate(raw_chunks):
                emb = self.generate_mock_embedding(raw_chunk)
                chunk = DbKnowledgeChunk(
                    document_id=doc.id,
                    content=raw_chunk,
                    embedding_json={"vector": emb},
                    metadata_json={"chunk_index": idx}
                )
                session.add(chunk)
                
            await session.commit()
            return doc

# Global ingestion engine instance
ingestion_engine = DocumentIngestionEngine()
