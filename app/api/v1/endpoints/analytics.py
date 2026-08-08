from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import User
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "mostRequestedFlat": "3 BHK Tower B",
        "avgBuyerBudgetLakhs": 115.5,
        "topObjections": [
            {"objection": "Price Negotiation", "percentage": 45},
            {"objection": "Possession Date Timeline", "percentage": 30},
            {"objection": "Bank Loan Approval", "percentage": 25}
        ],
        "peakEnquiryHours": [
            {"hour": "10 AM - 12 PM", "count": 142},
            {"hour": "6 PM - 9 PM", "count": 210}
        ],
        "bhkDemand": [
            {"config": "2 BHK", "count": 320, "percentage": 40},
            {"config": "3 BHK", "count": 380, "percentage": 47.5},
            {"config": "4 BHK", "count": 100, "percentage": 12.5}
        ],
        "conversionFunnel": [
            {"stage": "AI Chat Enquiries", "count": 1250, "rate": 100},
            {"stage": "Qualified Leads", "count": 680, "rate": 54.4},
            {"stage": "Site Visit Booked", "count": 210, "rate": 30.8},
            {"stage": "Closed Deals", "count": 48, "rate": 22.8}
        ]
    }
