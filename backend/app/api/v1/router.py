from fastapi import APIRouter
from app.api.v1.endpoints import (
    health, ai_hub, auth, admin, monitoring, incident,
    analysis, remediation, generation, secops, notification,
    workflow, dashboard, widget, websocket, analytics,
    integration, plugin, ops, aiops, agents, rag, finops,
    governance, automation, mobile, edge, mlops, lts
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(ai_hub.router, prefix="/ai-hub", tags=["ai-hub"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(incident.router, prefix="/incident", tags=["incident"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(remediation.router, prefix="/remediation", tags=["remediation"])
api_router.include_router(generation.router, prefix="/generation", tags=["generation"])
api_router.include_router(secops.router, prefix="/secops", tags=["secops"])
api_router.include_router(notification.router, prefix="/notification", tags=["notification"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(widget.router, prefix="/widget", tags=["widget"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(integration.router, prefix="/integration", tags=["integration"])
api_router.include_router(plugin.router, prefix="/plugin", tags=["plugin"])
api_router.include_router(ops.router, prefix="/ops", tags=["ops"])
api_router.include_router(aiops.router, prefix="/aiops", tags=["aiops"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(finops.router, prefix="/finops", tags=["finops"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])
api_router.include_router(mobile.router, prefix="/mobile", tags=["mobile"])
api_router.include_router(edge.router, prefix="/edge", tags=["edge"])
api_router.include_router(mlops.router, prefix="/mlops", tags=["mlops"])
api_router.include_router(lts.router, prefix="/lts", tags=["lts"])
