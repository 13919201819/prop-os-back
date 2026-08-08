from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import SiteVisitBooking, User
from app.core.deps import get_current_user
from pydantic import BaseModel
from datetime import date
from uuid import UUID

router = APIRouter()

class SiteVisitCreate(BaseModel):
    lead_id: UUID
    project_id: UUID
    buyer_name: str
    buyer_phone: str
    buyer_email: str
    visit_date: date
    visit_time: str
    visitors_count: int = 1
    notes: str = ""

@router.get("/")
async def list_site_visits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(SiteVisitBooking).where(SiteVisitBooking.tenant_id == current_user.tenant_id).order_by(SiteVisitBooking.visit_date.asc())
    )
    return result.scalars().all()

@router.post("/")
async def create_site_visit(
    booking_in: SiteVisitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_booking = SiteVisitBooking(
        tenant_id=current_user.tenant_id,
        **booking_in.dict()
    )
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking
