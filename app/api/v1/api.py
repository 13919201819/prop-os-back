from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    projects,
    flats,
    leads,
    site_visits,
    payments,
    widget,
    ai_chat,
    analytics,
    team
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects Catalog"])
api_router.include_router(flats.router, prefix="/flats", tags=["Inventory Units"])
api_router.include_router(leads.router, prefix="/leads", tags=["Lead Management CRM"])
api_router.include_router(site_visits.router, prefix="/site-visits", tags=["Site Visit Appointments"])
api_router.include_router(payments.router, prefix="/payments", tags=["Subscriptions & Payments"])
api_router.include_router(widget.router, prefix="/widget", tags=["AI Widget Configuration"])
api_router.include_router(ai_chat.router, prefix="/ai", tags=["AI Assistant RAG Engine"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Conversion Insights"])
api_router.include_router(team.router, prefix="/team", tags=["Sales Team Management"])

