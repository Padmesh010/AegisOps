from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.integration import DbIntegrationAccount
from app.services.integration.sync import inventory_synchronizer
from app.services.integration.cost import cost_optimizer

router = APIRouter()

@router.post("/accounts", status_code=201)
async def register_cloud_account(
    name: str,
    provider: str,  # aws, gcp, azure
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    account = DbIntegrationAccount(
        provider_type=provider,
        account_name=name,
        encrypted_credentials="mock_encrypted_secret"
    )
    db.add(account)
    await db.commit()
    return {"status": "registered", "account_id": str(account.id)}

@router.post("/accounts/{account_id}/sync", response_model=dict)
async def trigger_inventory_sync(
    account_id: str,
    user: Any = Depends(get_current_user)
) -> dict:
    success = await inventory_synchronizer.synchronize_account_inventory(account_id)
    return {"status": "success" if success else "failed"}

@router.get("/accounts/{account_id}/costs", response_model=list[dict])
async def get_cost_recommendations(
    account_id: str,
    user: Any = Depends(get_current_user)
) -> list[dict]:
    recs = await cost_optimizer.analyze_account_costs(account_id)
    return [
        {
            "id": str(r.id),
            "recommendation_type": r.recommendation_type,
            "savings_pct": r.savings_pct,
            "steps": r.action_steps
        } for r in recs
    ]

from typing import Any
