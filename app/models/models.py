import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Numeric, Boolean, Text, DateTime, Date, ForeignKey, JSON, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    plan: Mapped[str] = mapped_column(String(50), default="Growth", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Active", nullable=False)
    total_projects: Mapped[int] = mapped_column(Integer, default=0)
    total_leads: Mapped[int] = mapped_column(Integer, default=0)
    monthly_conversations: Mapped[int] = mapped_column(Integer, default=0)
    max_conversations: Mapped[int] = mapped_column(Integer, default=5000)
    member_count: Mapped[int] = mapped_column(Integer, default=1)
    joined_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    users: Mapped[List["User"]] = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="tenant", cascade="all, delete-orphan")
    leads: Mapped[List["Lead"]] = relationship("Lead", back_populates="tenant", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False) # 'super_admin', 'builder_admin', 'sales_exec', 'buyer'
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tagline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    rera_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Under Construction")
    total_units: Mapped[int] = mapped_column(Integer, default=0)
    available_units: Mapped[int] = mapped_column(Integer, default=0)
    price_range_str: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    min_price_lakhs: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    max_price_lakhs: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    possession_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    amenities: Mapped[dict] = mapped_column(JSONB, default=list)
    nearby_highlights: Mapped[dict] = mapped_column(JSONB, default=dict)
    banks: Mapped[dict] = mapped_column(JSONB, default=list)
    gallery_images: Mapped[dict] = mapped_column(JSONB, default=list)
    faqs: Mapped[dict] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="projects")
    flats: Mapped[List["Flat"]] = relationship("Flat", back_populates="project", cascade="all, delete-orphan")


class Flat(Base):
    __tablename__ = "flats"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    unit_number: Mapped[str] = mapped_column(String(50), nullable=False)
    tower: Mapped[str] = mapped_column(String(50), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    config: Mapped[str] = mapped_column(String(50), nullable=False) # '1 BHK', '2 BHK', '3 BHK', etc.
    area_sq_ft: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price_lakhs: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    facing: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    balconies: Mapped[int] = mapped_column(Integer, default=1)
    parking_spots: Mapped[int] = mapped_column(Integer, default=1)
    view_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    possession_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Available") # 'Available', 'Reserved', 'Sold'
    floor_plan_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    images: Mapped[dict] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    project: Mapped["Project"] = relationship("Project", back_populates="flats")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    assigned_sales_exec_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    budget_range_str: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    budget_lakhs: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    preferred_config: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timeline: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    loan_required: Mapped[bool] = mapped_column(Boolean, default=False)
    use_type: Mapped[str] = mapped_column(String(50), default="Self Use")
    visit_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    lead_score: Mapped[str] = mapped_column(String(20), default="WARM") # 'HOT', 'WARM', 'COLD'
    score_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(100), default="AI Web Widget")
    status: Mapped[str] = mapped_column(String(50), default="New") # 'New', 'Contacted', 'Site Visit Booked', etc.
    conversation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="leads")


class SiteVisitBooking(Base):
    __tablename__ = "site_visit_bookings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assigned_sales_exec_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    buyer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    buyer_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    buyer_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    visit_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    visit_time: Mapped[str] = mapped_column(String(50), nullable=False)
    visitors_count: Mapped[int] = mapped_column(Integer, default=1)
    preferred_config: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Confirmed") # 'Confirmed', 'Completed', etc.
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    invoice_no: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan_id: Mapped[str] = mapped_column(String(50), nullable=False) # 'starter', 'growth', 'enterprise'
    plan_name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    base_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    gstin: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    vat_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
