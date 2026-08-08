from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    lead_id: Optional[str] = None
    project_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    recommended_flats: List[dict] = []
    actions: List[str] = []

@router.post("/chat", response_model=ChatResponse)
async def ai_chat_assistant(request: ChatRequest):
    # Simulated RAG response combining Project documents & Flat inventory matching
    return ChatResponse(
        reply=f"Thank you for reaching out! Based on your interest in properties, I found great matches for '{request.message}'. Would you like to schedule a site visit?",
        recommended_flats=[
          {"unit": "A-402", "config": "3 BHK", "priceLakhs": 125, "tower": "Tower A"}
        ],
        actions=["Book Site Visit", "Download Brochure", "Call Sales Rep"]
    )
