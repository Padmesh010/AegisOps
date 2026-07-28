from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.infrastructure.db.models.mlops import DbMLRun
from app.services.mlops.registry import mlops_registry
from app.services.mlops.prompt import prompt_template_manager
from app.services.mlops.evaluator import model_evaluator

router = APIRouter()

@router.post("/prompts", response_model=dict)
async def register_prompt_version(
    key: str,
    version: str,
    template: str,
    params: dict = {},
    user: Any = Depends(get_current_user)
) -> dict:
    pv = await prompt_template_manager.create_prompt_version(key, version, template, params)
    return {"status": "registered", "prompt_id": str(pv.id), "key": pv.prompt_key}

@router.post("/prompts/{key}/format", response_model=dict)
async def format_prompt_template(
    key: str,
    variables: dict,
    template_str: str,
    user: Any = Depends(get_current_user)
) -> dict:
    formatted = prompt_template_manager.format_prompt(template_str, variables)
    return {"formatted_prompt": formatted}

@router.post("/experiments/run", response_model=dict)
async def log_experiment_run(
    experiment_name: str,
    prompt_version_id: str,
    model_name: str,
    metrics: dict,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user)
) -> dict:
    run = DbMLRun(
        experiment_name=experiment_name,
        prompt_version_id=uuid.UUID(prompt_version_id),
        model_name=model_name,
        metrics_json=metrics
    )
    db.add(run)
    await db.commit()
    return {"status": "logged", "run_id": str(run.id)}

@router.post("/deployments/canary", response_model=dict)
async def deploy_model_canary(
    model_name: str,
    stage: str,
    traffic_pct: int,
    user: Any = Depends(get_current_user)
) -> dict:
    deployment = await mlops_registry.configure_canary_deployment(model_name, stage, traffic_pct)
    return {"status": "deployed", "model": deployment.model_name, "stage": deployment.deployment_stage}

from typing import Any
