import numpy as np
from typing import List, Tuple, Dict, Any

class InMemoryVectorDatabase:
    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate the standard cosine similarity metrics score between float arrays."""
        a = np.array(vec_a)
        b = np.array(vec_b)
        
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
            
        return float(np.dot(a, b) / (norm_a * norm_b))

    def query_similarity(self, query_vector: List[float], candidate_chunks: List[Dict[str, Any]], top_k: int = 3) -> List[Tuple[float, Dict[str, Any]]]:
        """Iterate candidates list and score similarity indexes, returning top_k matches sorted descending."""
        scored = []
        for chunk in candidate_chunks:
            chunk_vector = chunk.get("embedding", [])
            if not chunk_vector:
                continue
            sim = self.cosine_similarity(query_vector, chunk_vector)
            scored.append((sim, chunk))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

# Global database instance
vector_db = InMemoryVectorDatabase()
