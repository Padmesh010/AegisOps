import numpy as np
import logging
from typing import List, Dict, Any

logger = logging.getLogger("app.services.aiops.anomaly")

class AnomalyDetectionEngine:
    def detect_zscore(self, history: List[float], threshold: float = 3.0) -> Dict[str, Any]:
        """Perform statistical Z-score checks on historical floats metric list."""
        if len(history) < 3:
            return {"anomalous": False, "reason": "Insufficient points"}
            
        data = np.array(history)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0.0:
            return {"anomalous": False, "reason": "Flatline sequence"}
            
        latest = history[-1]
        z_score = abs((latest - mean) / std)
        
        return {
            "anomalous": bool(z_score > threshold),
            "score": float(z_score),
            "latest_value": latest,
            "mean": float(mean),
            "std": float(std)
        }

    def detect_isolation_forest(self, history: List[float], contamination: float = 0.05) -> Dict[str, Any]:
        """Detect anomalies using Isolation Forest strategy, falling back to Z-score on import errors."""
        try:
            from sklearn.ensemble import IsolationForest
            if len(history) < 10:
                return self.detect_zscore(history)
                
            data = np.array(history).reshape(-1, 1)
            clf = IsolationForest(contamination=contamination, random_state=42)
            clf.fit(data)
            
            # Predict last value
            pred = clf.predict([[history[-1]]])[0]  # -1 for anomaly, 1 for normal
            
            return {
                "anomalous": bool(pred == -1),
                "score": float(clf.score_samples([[history[-1]]])[0]),
                "latest_value": history[-1]
            }
        except ImportError:
            logger.warning("scikit-learn not available. Falling back to Z-score anomaly checks.")
            return self.detect_zscore(history)

# Global engine instance
anomaly_engine = AnomalyDetectionEngine()
