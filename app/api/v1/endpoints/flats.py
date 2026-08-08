from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Flat, User
from app.schemas.schemas import FlatCreate, FlatResponse
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[FlatResponse])
async def list_flats(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Flat).where(Flat.tenant_id == current_user.tenant_id)
    if project_id:
        query = query.where(Flat.project_id == project_id)
    if status:
        query = query.where(Flat.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=FlatResponse)
async def create_flat(
    flat_in: FlatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_flat = Flat(
        tenant_id=current_user.tenant_id,
        **flat_in.dict()
    )
    db.add(new_flat)
    await db.commit()
    await db.refresh(new_flat)
    return new_flat

@router.patch("/{flat_id}/status")
async def update_flat_status(
    flat_id: str,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Flat).where(Flat.id == flat_id, Flat.tenant_id == current_user.tenant_id)
    )
    flat = result.scalars().first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found")
    
    flat.status = status
    await db.commit()
    return {"status": "success", "message": f"Flat status updated to {status}"}
