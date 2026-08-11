import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from pydantic import BaseModel
from typing import Dict, Any, Optional

logger = logging.getLogger("propos.widget")
router = APIRouter()

class WidgetConfigSchema(BaseModel):
    theme_color: Optional[str] = "brand"
    position: Optional[str] = "bottom-right"
    agent_name: Optional[str] = "PropSales AI"
    greeting_text: Optional[str] = "Hello! Looking for your dream property?"
    primary_hex: Optional[str] = "#2563EB"
    enabled_features: Optional[Dict[str, bool]] = {
        "chat": True, "voice": True, "recommend": True, "compare": True, "booking": True
    }

@router.get("/")
async def get_widget_config(
    tenant_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching widget configuration for tenant_id: {tenant_id or 'default'}")
    return {
        "themeColor": "brand",
        "position": "bottom-right",
        "agentName": "PropSales AI",
        "greetingText": "Hello! Looking for your dream property?",
        "primaryHex": "#2563EB",
        "enabledFeatures": {
            "chat": True, "voice": True, "recommend": True, "compare": True, "booking": True
        }
    }

@router.put("/")
@router.post("/")
async def update_widget_config(
    config_in: WidgetConfigSchema,
    tenant_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Updating widget configuration for tenant_id: {tenant_id or 'default'}: {config_in}")
    return {
        "status": "success",
        "tenant_id": tenant_id or "default",
        "config": config_in.model_dump()
    }
