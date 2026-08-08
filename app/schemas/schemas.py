from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID

# Auth & User Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "builder_admin"
    tenant_name: Optional[str] = "My Real Estate Builder"

class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    email: EmailStr
    role: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

# Tenant Schema
class TenantResponse(BaseModel):
    id: UUID
    name: str
    logo_url: Optional[str] = None
    plan: str
    status: str
    total_projects: int
    total_leads: int
    monthly_conversations: int
    max_conversations: int

    class Config:
        from_attributes = True

# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    tagline: Optional[str] = None
    location: str
    city: str
    rera_id: Optional[str] = None
    status: str = "Under Construction"
    min_price_lakhs: float
    max_price_lakhs: float
    possession_date: Optional[date] = None
    amenities: List[str] = []

class ProjectResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    tagline: Optional[str] = None
    location: str
    city: str
    rera_id: Optional[str] = None
    status: str
    total_units: int
    available_units: int
    min_price_lakhs: float
    max_price_lakhs: float
    amenities: List[str] = []

    class Config:
        from_attributes = True

# Flat Schemas
class FlatCreate(BaseModel):
    project_id: UUID
    unit_number: str
    tower: str
    floor: int
    config: str
    area_sq_ft: float
    price_lakhs: float
    facing: Optional[str] = "East"

class FlatResponse(BaseModel):
    id: UUID
    project_id: UUID
    unit_number: str
    tower: str
    floor: int
    config: str
    area_sq_ft: float
    price_lakhs: float
    facing: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

# Lead Schemas
class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    project_id: Optional[UUID] = None
    preferred_config: Optional[str] = None
    budget_lakhs: Optional[float] = None
    source: str = "AI Web Widget"

class LeadResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    phone: str
    email: Optional[str] = None
    lead_score: str
    score_reason: Optional[str] = None
    source: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Sales Executive Schemas
class SalesExecCreate(BaseModel):
    name: str
    role: str = "Senior Executive"
    avatar_url: Optional[str] = None
    deals_closed: int = 0
    sales_revenue_cr: float = 0.0
    conversion_rate: str = "85%"
    avg_response_time: str = "2 mins"
    badge: Optional[str] = "🏆 Sales Specialist"

class SalesExecResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    role: str
    avatar_url: Optional[str] = None
    deals_closed: int
    sales_revenue_cr: float
    conversion_rate: str
    avg_response_time: str
    badge: Optional[str] = None

    class Config:
        from_attributes = True

