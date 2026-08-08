from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db
from app.schemas.schemas import SalesExecCreate, SalesExecResponse

router = APIRouter()

# Default mock sales executives response when database is in dynamic RPC fallback
MOCK_EXECUTIVES = [
    {
        "id": "10101010-1010-1010-1010-101010101010",
        "tenant_id": "11111111-1111-1111-1111-111111111111",
        "name": "Rohan Sharma",
        "role": "Senior Sales Manager",
        "avatar_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=200",
        "deals_closed": 12,
        "sales_revenue_cr": 18.40,
        "conversion_rate": "94%",
        "avg_response_time": "2 mins",
        "badge": "🏆 Top Closer of Month"
    },
    {
        "id": "20202020-2020-2020-2020-202020202020",
        "tenant_id": "11111111-1111-1111-1111-111111111111",
        "name": "Priya Mehta",
        "role": "Luxury Housing Specialist",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=200",
        "deals_closed": 10,
        "sales_revenue_cr": 14.80,
        "conversion_rate": "91%",
        "avg_response_time": "3 mins",
        "badge": "🌟 High Customer CSAT"
    },
    {
        "id": "30303030-3030-3030-3030-303030303030",
        "tenant_id": "11111111-1111-1111-1111-111111111111",
        "name": "Vikram Malhotra",
        "role": "Penthouse & Villa Specialist",
        "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=200",
        "deals_closed": 8,
        "sales_revenue_cr": 11.20,
        "conversion_rate": "88%",
        "avg_response_time": "4 mins",
        "badge": "💎 Highest Ticket Avg"
    },
    {
        "id": "40404040-4040-4040-4040-404040404040",
        "tenant_id": "11111111-1111-1111-1111-111111111111",
        "name": "Ankit Verma",
        "role": "Junior Sales Associate",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200",
        "deals_closed": 4,
        "sales_revenue_cr": 4.20,
        "conversion_rate": "82%",
        "avg_response_time": "5 mins",
        "badge": "🚀 Rising Star"
    }
]

@router.get("/executives", response_model=List[SalesExecResponse])
def get_team_executives(tenant_id: UUID = UUID("11111111-1111-1111-1111-111111111111"), db: Session = Depends(get_db)):
    """Fetch sales executive team members for builder tenant"""
    return MOCK_EXECUTIVES

@router.post("/executives", response_model=SalesExecResponse, status_code=status.HTTP_201_CREATED)
def create_team_executive(exec_in: SalesExecCreate, tenant_id: UUID = UUID("11111111-1111-1111-1111-111111111111"), db: Session = Depends(get_db)):
    """Add new sales executive to builder team"""
    import uuid
    new_exec = {
        "id": str(uuid.uuid4()),
        "tenant_id": str(tenant_id),
        "name": exec_in.name,
        "role": exec_in.role,
        "avatar_url": exec_in.avatar_url or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=120",
        "deals_closed": exec_in.deals_closed,
        "sales_revenue_cr": exec_in.sales_revenue_cr,
        "conversion_rate": exec_in.conversion_rate,
        "avg_response_time": exec_in.avg_response_time,
        "badge": exec_in.badge
    }
    return new_exec
