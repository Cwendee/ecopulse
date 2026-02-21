from fastapi import APIRouter
from app.models.schemas import (
    LocationResolveRequest,
    LocationResolveResponse
)

router = APIRouter()


@router.post("/location/resolve", response_model=LocationResolveResponse)
def resolve_location(data: LocationResolveRequest):
    return {
        "region_id": "NG-LA-IKJ",
        "region_name": "Ikeja",
        "country": "Nigeria"
    }