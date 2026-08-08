from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import User
from app.core.deps import get_current_user
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class WidgetConfigSchema(BaseModel):
    theme_color: str = "brand"
    position: str = "bottom-right"
    agent_name: str = "PropSales AI"
    greeting_text: str = "Hello! Looking for your dream property?"
    primary_hex: str = "#2563EB"
    enabled_features: Dict[str, bool] = {"chat": True, "voice": True, "recommend": True, "compare": True, "booking": True}

@router.get("/")
async def get_widget_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "themeColor": "brand",
        "position": "bottom-right",
        "agentName": "PropSales AI",
        "greetingText": "Hello! Looking for your dream property?",
        "primaryHex": "#2563EB",
        "enabledFeatures": {"chat": True, "voice": True, "recommend": True, "compare": True, "booking": True}
    }

@router.put("/")
async def update_widget_config(
    config_in: WidgetConfigSchema,
    current_user: User = Depends(get_current_user)
):
    return {"status": "success", "config": config_in}
