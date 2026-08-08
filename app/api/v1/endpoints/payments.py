from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import PaymentTransaction, User
from app.core.deps import get_current_user
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class PaymentInitRequest(BaseModel):
    plan_id: str
    plan_name: str
    amount: float
    currency: str = "INR"
    payment_method: str

@router.get("/")
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(PaymentTransaction).where(PaymentTransaction.tenant_id == current_user.tenant_id).order_by(PaymentTransaction.created_at.desc())
    )
    return result.scalars().all()

@router.post("/checkout")
async def create_checkout_session(
    payment_in: PaymentInitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import uuid
    invoice_no = f"INV-{uuid.uuid4().hex[:8].upper()}"
    tax_amount = round(payment_in.amount * 0.18, 2)
    base_amount = payment_in.amount - tax_amount

    transaction = PaymentTransaction(
        tenant_id=current_user.tenant_id,
        invoice_no=invoice_no,
        plan_id=payment_in.plan_id,
        plan_name=payment_in.plan_name,
        region="india" if payment_in.currency == "INR" else "international",
        amount=payment_in.amount,
        base_amount=base_amount,
        tax_amount=tax_amount,
        currency=payment_in.currency,
        payment_method=payment_in.payment_method,
        status="SUCCESS", # Simulated gateway response
        customer_name=current_user.name,
        customer_email=current_user.email,
        company_name="Builder Corp"
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction
