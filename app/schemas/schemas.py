from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID

# Auth & User Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email_valid: bool = True
    password_valid: bool = True
    user: Optional[Dict[str, Any]] = None
    message: Optional[str] = "Authentication successful"

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
    password_hash: Optional[str] = None
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str

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
    status: Optional[str] = "Under Construction"
    total_units: Optional[int] = 0
    available_units: Optional[int] = 0
    min_price_lakhs: Optional[float] = 0.0
    max_price_lakhs: Optional[float] = 0.0
    amenities: Optional[List[str]] = []

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
    status: Optional[str] = "Available"

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
    source: Optional[str] = "AI Web Widget"

class LeadResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    phone: str
    email: Optional[str] = None
    lead_score: Optional[str] = "WARM"
    score_reason: Optional[str] = None
    source: Optional[str] = "AI Web Widget"
    status: Optional[str] = "New"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Sales Executive Schemas
class SalesExecCreate(BaseModel):
    name: str
    role: Optional[str] = "Senior Executive"
    avatar_url: Optional[str] = None
    deals_closed: Optional[int] = 0
    sales_revenue_cr: Optional[float] = 0.0
    conversion_rate: Optional[str] = "85%"
    avg_response_time: Optional[str] = "2 mins"
    badge: Optional[str] = "🏆 Sales Specialist"

class SalesExecResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    role: Optional[str] = "Senior Executive"
    avatar_url: Optional[str] = None
    deals_closed: Optional[int] = 0
    sales_revenue_cr: Optional[float] = 0.0
    conversion_rate: Optional[str] = "85%"
    avg_response_time: Optional[str] = "2 mins"
    badge: Optional[str] = None

    class Config:
        from_attributes = True


