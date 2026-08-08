from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Project, User
from app.schemas.schemas import ProjectCreate, ProjectResponse
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.tenant_id == current_user.tenant_id))
    return result.scalars().all()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_project = Project(
        tenant_id=current_user.tenant_id,
        **project_in.dict()
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project
