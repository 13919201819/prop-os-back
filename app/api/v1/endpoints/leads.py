from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Lead, User
from app.schemas.schemas import LeadCreate, LeadResponse
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Lead).where(Lead.tenant_id == current_user.tenant_id).order_by(Lead.created_at.desc())
    )
    return result.scalars().all()

@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead_in: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_lead = Lead(
        tenant_id=current_user.tenant_id,
        **lead_in.dict()
    )
    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)
    return new_lead
