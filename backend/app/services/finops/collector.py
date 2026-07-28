import logging
from typing import List, Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.finops import DbCostRecord

logger = logging.getLogger("app.services.finops.collector")

class CostCollectorEngine:
    async def synchronize_aws_billing(self, account_id: str) -> List[DbCostRecord]:
        """Mock pulling billing records from AWS Cost Explorer APIs, writing entries to Postgres."""
        records_mock = [
            {"resource_id": "i-0123456789abcdef0", "service_type": "compute", "cost": 45.5, "tags": {"team": "ops"}},
            {"resource_id": "vol-0123456789abcdef0", "service_type": "storage", "cost": 12.0, "tags": {"team": "ops"}},
            {"resource_id": "db-prod-postgres", "service_type": "database", "cost": 150.0, "tags": {"team": "dev"}}
        ]
        
        saved_records = []
        async with TestingSessionLocal() as session:
            for r in records_mock:
                rec = DbCostRecord(
                    provider="aws",
                    resource_id=r["resource_id"],
                    service_type=r["service_type"],
                    cost_amount=r["cost"],
                    tags_json=r["tags"]
                )
                session.add(rec)
                saved_records.append(rec)
            await session.commit()
            
        logger.info(f"Synchronized {len(saved_records)} AWS cost records for account {account_id}")
        return saved_records

# Global collector instance
cost_collector = CostCollectorEngine()
