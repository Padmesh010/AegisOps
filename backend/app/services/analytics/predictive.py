import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

class CapacityForecaster:
    def forecast_resource_exhaustion(self, history: List[Tuple[float, float]], threshold: float) -> float:
        """Run linear regression on historical metrics (timestamp, value). Return estimated time remaining in hours."""
        if len(history) < 5:
            # Insufficient data points to perform regression
            return -1.0
            
        times = [pt[0] for pt in history]
        values = [pt[1] for pt in history]
        
        # Calculate slope and intercept
        x = np.array(times)
        y = np.array(values)
        
        A = np.vstack([x, np.ones(len(x))]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        
        # If resource usage is declining, it will never exceed the threshold
        if slope <= 0:
            return 9999.0
            
        # Target threshold time
        target_time = (threshold - intercept) / slope
        time_diff_sec = target_time - times[-1]
        
        return max(0.0, float(time_diff_sec / 3600.0))  # return in hours

# Global forecaster instance
capacity_forecaster = CapacityForecaster()
