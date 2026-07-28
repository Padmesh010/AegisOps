import numpy as np
import logging
from typing import List, Tuple, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.aiops import DbCapacityForecast

logger = logging.getLogger("app.services.aiops.forecaster")

class CapacityForecastEngine:
    async def forecast_exhaustion(
        self,
        resource_type: str,
        target_id: str,
        history: List[Tuple[float, float]],  # list of (timestamp, value)
        threshold: float
    ) -> DbCapacityForecast:
        """Run polynomial trend fitting, project exhaustion window in hours, and persist results."""
        if len(history) < 5:
            # Fallback default values
            return DbCapacityForecast(
                resource_type=resource_type,
                target_id=target_id,
                forecast_window_hours=24,
                growth_rate_pct=0.0,
                estimated_exhaustion_hours=-1.0
            )
            
        times = np.array([pt[0] for pt in history])
        values = np.array([pt[1] for pt in history])
        
        # Fit 1st degree polynomial (linear fit)
        slope, intercept = np.polyfit(times, values, 1)
        
        # Calculate growth rate relative to last value
        latest_val = values[-1]
        growth = float(slope * 3600.0)  # growth per hour
        growth_pct = float((growth / latest_val) * 100.0) if latest_val > 0 else 0.0
        
        est_hours = -1.0
        if slope > 0:
            target_time = (threshold - intercept) / slope
            diff_sec = target_time - times[-1]
            est_hours = max(0.0, float(diff_sec / 3600.0))
            
        async with TestingSessionLocal() as session:
            forecast = DbCapacityForecast(
                resource_type=resource_type,
                target_id=target_id,
                forecast_window_hours=24,
                growth_rate_pct=growth_pct,
                estimated_exhaustion_hours=est_hours,
                confidence_lower=est_hours * 0.8 if est_hours > 0 else 0.0,
                confidence_upper=est_hours * 1.2 if est_hours > 0 else 0.0
            )
            session.add(forecast)
            await session.commit()
            return forecast

# Global forecaster instance
forecast_engine = CapacityForecastEngine()
