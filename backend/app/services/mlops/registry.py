import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.mlops import DbModelDeployment

logger = logging.getLogger("app.services.mlops.registry")

class MLOpsModelRegistry:
    async def configure_canary_deployment(self, model_name: str, stage: str, traffic_pct: int) -> DbModelDeployment:
        """Create or update model deployment stages and traffic splits details in database."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(DbModelDeployment).where(DbModelDeployment.model_name == model_name)
            )
            deployment = res.scalar_one_or_none()
            
            if deployment:
                deployment.deployment_stage = stage
                deployment.target_traffic_pct = traffic_pct
            else:
                deployment = DbModelDeployment(
                    model_name=model_name,
                    deployment_stage=stage,
                    target_traffic_pct=traffic_pct,
                    status="active"
                )
            session.add(deployment)
            await session.commit()
            return deployment

# Global MLOps registry instance
mlops_registry = MLOpsModelRegistry()
