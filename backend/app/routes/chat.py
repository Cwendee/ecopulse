from fastapi import APIRouter
from app.models.schemas import EcoChatRequest, EcoChatResponse

router = APIRouter()


@router.post("/eco/chat", response_model=EcoChatResponse)
def eco_chat(data: EcoChatRequest):
    # Placeholder response for MVP
    return {
        "reply": "Current risk level for your region is medium. Stay alert for heavy rainfall.",
        "risk_level": "medium"
    }