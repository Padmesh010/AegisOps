import logging
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.metric import DbAlertThreshold
from app.services.incident.manager import incident_manager

logger = logging.getLogger("app.services.incident.evaluator")

class AlertEvaluator:
    async def evaluate_metrics(self, target_id: str, metrics: dict) -> None:
        """Evaluate raw metric updates against threshold settings, generating alerts."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbAlertThreshold))
            thresholds = res.scalars().all()
            
            for threshold in thresholds:
                metric_name = threshold.metric_name
                if metric_name in metrics:
                    value = metrics[metric_name]
                    
                    # 1. Critical Limit Breach Check
                    if value >= threshold.critical_limit:
                        logger.warn(f"CRITICAL breach on {target_id} - {metric_name}: {value} (Limit: {threshold.critical_limit})")
                        await incident_manager.trigger_incident(
                            title=f"Critical Threshold Breach on {metric_name}",
                            severity="critical",
                            description=f"Resource {target_id} reported {metric_name} value {value:.2f} exceeding critical limit of {threshold.critical_limit:.2f}"
                        )
                    # 2. Warning Limit Breach Check
                    elif value >= threshold.warning_limit:
                        logger.info(f"Warning breach on {target_id} - {metric_name}: {value} (Limit: {threshold.warning_limit})")
                        await incident_manager.trigger_incident(
                            title=f"Warning Threshold Breach on {metric_name}",
                            severity="warning",
                            description=f"Resource {target_id} reported {metric_name} value {value:.2f} exceeding warning limit of {threshold.warning_limit:.2f}"
                        )

# Global evaluator instance
alert_evaluator = AlertEvaluator()
