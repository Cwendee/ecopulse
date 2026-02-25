from pydantic import BaseModel


class LocationResolveRequest(BaseModel):
    latitude: float
    longitude: float


class LocationResolveResponse(BaseModel):
    region_id: str
    region_name: str
    country: str


class RiskResponse(BaseModel):
    region_id: str
    region_name: str
    country: str
    rainfall_index: float
    anomaly: float
    rainfall_percentile: float
    risk_level: str
    rainfall_unusually_high: bool
    anomaly_large: bool
    data_quality: str
    valid_at: str


class EcoChatRequest(BaseModel):
    message: str
    region_id: str


class EcoChatResponse(BaseModel):
    reply: str
    risk_level: str