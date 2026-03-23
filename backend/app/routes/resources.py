from fastapi import APIRouter
from Datapipeline.local_resources import get_resources_for_location

router = APIRouter()

@router.get("/countries/{country_code}/resources")
def get_country_resources(country_code: str):
    return get_resources_for_location(country_iso3=country_code)