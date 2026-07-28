from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Any
from app.api.dependencies import get_current_user
from app.services.lts.hardening import lts_hardening_engine
from app.services.lts.diagnostics import diagnostic_bundle_service

router = APIRouter()

@router.get("/diagnostics/bundle")
async def download_diagnostics_bundle(
    user: Any = Depends(get_current_user)
) -> Response:
    """Collect system logs, package them into a compressed ZIP stream, and download."""
    zip_bytes = diagnostic_bundle_service.create_log_bundle()
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=aegisops_diagnostics.zip"}
    )

@router.post("/shutdown", response_model=dict)
async def shutdown_server(
    user: Any = Depends(get_current_user)
) -> dict:
    """Initiate server graceful shutdown routines."""
    import asyncio
    asyncio.create_task(lts_hardening_engine.initiate_graceful_shutdown())
    return {"status": "shutting_down", "message": "Server graceful shutdown initiated."}
