import logging
from typing import Dict, Any

logger = logging.getLogger("app.services.mlops.monitor")

class ModelPerformanceMonitor:
    def __init__(self) -> None:
        self._usage_cache: Dict[str, Dict[str, Any]] = {}

    def log_model_invocation(self, model_name: str, input_tokens: int, output_tokens: int, latency_ms: float) -> None:
        """Cache model execution stats, summing token volumes and calculating averages."""
        if model_name not in self._usage_cache:
            self._usage_cache[model_name] = {"total_inputs": 0, "total_outputs": 0, "latencies": []}
            
        stats = self._usage_cache[model_name]
        stats["total_inputs"] += input_tokens
        stats["total_outputs"] += output_tokens
        stats["latencies"].append(latency_ms)
        
        # Calculate cost estimate: 0.001 per 1K input, 0.002 per 1K output
        cost_est = (input_tokens * 0.001 / 1000.0) + (output_tokens * 0.002 / 1000.0)
        logger.info(f"Model {model_name} invocation logged. Est cost: ${cost_est:.6f} | Latency: {latency_ms}ms")

# Global monitor instance
model_performance_monitor = ModelPerformanceMonitor()
