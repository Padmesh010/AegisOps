import logging
from typing import List, Dict, Any

logger = logging.getLogger("app.services.rag.context_builder")

class ContextBuilder:
    def assemble_prompt_context(self, retrieved_chunks: List[Dict[str, Any]], char_budget: int = 4000) -> str:
        """Accumulate chunk text fragments into formatted context window strings, staying within budget limits."""
        context_parts = []
        current_length = 0
        
        for idx, chunk in enumerate(retrieved_chunks, 1):
            content = chunk.get("content", "")
            meta = chunk.get("metadata", {})
            
            # Format fragment card
            card = f"[Source Document Chunk {idx} (Index: {meta.get('chunk_index', 0)})]:\n{content}\n\n"
            if current_length + len(card) > char_budget:
                logger.info(f"Token budget reached. Skipping remaining {len(retrieved_chunks) - idx + 1} chunks.")
                break
                
            context_parts.append(card)
            current_length += len(card)
            
        return "".join(context_parts)

# Global builder instance
context_builder = ContextBuilder()
