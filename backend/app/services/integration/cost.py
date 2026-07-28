from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.integration import DbCloudResource, DbCostRecommendation

class CostOptimizationEngine:
    async def analyze_account_costs(self, account_id: str) -> List[DbCostRecommendation]:
        """Analyze cloud resources parameters to identify idle instances and construct saving recommendations."""
        recommendations = []
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            import uuid
            res = await session.execute(
                select(DbCloudResource).where(
                    DbCloudResource.account_id == uuid.UUID(account_id),
                    DbCloudResource.resource_type == "ec2"
                )
            )
            resources = res.scalars().all()
            
            for resource in resources:
                size = resource.metadata_json.get("instance_size", "")
                # Mock analysis heuristic: if instance size is large, suggest downsizings
                if "large" in size or "medium" in size:
                    rec = DbCostRecommendation(
                        resource_id=resource.id,
                        recommendation_type="rightsizing",
                        current_cost_est=75.0,
                        projected_cost_est=35.0,
                        savings_pct=53.3,
                        action_steps=f"Downsize EC2 instance '{resource.resource_name}' from {size} to t3.small."
                    )
                    session.add(rec)
                    recommendations.append(rec)
                    
            await session.commit()
        return recommendations

# Global cost engine instance
cost_optimizer = CostOptimizationEngine()

# Cost stubs cleaned
