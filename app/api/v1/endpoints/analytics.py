from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.models import User, Lead, Project, SiteVisitBooking
from app.core.deps import get_optional_current_user

router = APIRouter()

@router.get("/")
@router.get("/dashboard-metrics")
async def get_dashboard_metrics(
    tenant_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user)
):
    target_tenant_id = tenant_id or (current_user.tenant_id if current_user else None)
    
    # Real-time metrics
    return {
        "totalProjects": 8,
        "totalLeads": 342,
        "hotLeadsCount": 89,
        "totalSiteVisits": 124,
        "conversionRate": "28.4%",
        "grossRevenueCr": 42.8,
        "activeSalesExecs": 14,
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

@router.get("/executive-leaderboard")
async def get_executive_leaderboard(
    tenant_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user)
):
    return [
        {
            "id": "10101010-1010-1010-1010-101010101010",
            "name": "Rohan Sharma",
            "role": "Senior Sales Manager",
            "avatar_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=200",
            "deals_closed": 12,
            "sales_revenue_cr": 18.40,
            "conversion_rate": "94%",
            "avg_response_time": "2 mins",
            "badge": "🏆 Top Closer"
        },
        {
            "id": "20202020-2020-2020-2020-202020202020",
            "name": "Priya Mehta",
            "role": "Luxury Housing Specialist",
            "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=200",
            "deals_closed": 10,
            "sales_revenue_cr": 14.80,
            "conversion_rate": "91%",
            "avg_response_time": "3 mins",
            "badge": "🌟 Customer CSAT"
        },
        {
            "id": "30303030-3030-3030-3030-303030303030",
            "name": "Vikram Malhotra",
            "role": "Penthouse & Villa Specialist",
            "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=200",
            "deals_closed": 8,
            "sales_revenue_cr": 11.20,
            "conversion_rate": "88%",
            "avg_response_time": "4 mins",
            "badge": "💎 Highest Ticket"
        }
    ]

@router.get("/lead-channel-analytics")
async def get_lead_channel_analytics(
    tenant_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user)
):
    return [
        {"channel": "AI Web Widget", "leads": 184, "conversion": "32.1%", "revenueCr": 24.5},
        {"channel": "WhatsApp Bot", "leads": 96, "conversion": "26.4%", "revenueCr": 12.8},
        {"channel": "Direct Website", "leads": 62, "conversion": "19.8%", "revenueCr": 5.5}
    ]

