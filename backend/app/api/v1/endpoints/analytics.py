from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_db_session
from app.services.analytics.kpi import kpi_calculator
from app.services.analytics.insights import insights_generator

router = APIRouter()

@router.get("/kpis/mttr", response_model=dict)
async def get_system_mttr(
    user: Any = Depends(get_current_user)
) -> dict:
    mttr = await kpi_calculator.calculate_incident_mttr()
    return {"mean_time_to_resolution_minutes": mttr}

@router.post("/reports/weekly", response_model=dict)
async def generate_weekly_report(
    incidents_count: int = 5,
    user: Any = Depends(get_current_user)
) -> dict:
    # Build standard KPI mocks payload
    kpi_data = {"platform_availability": 99.95, "remediation_success_rate": 88.0}
    report = await insights_generator.generate_weekly_report(kpi_data, incidents_count)
    return {"report_markdown": report}

from typing import Any
