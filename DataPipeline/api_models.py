from dataclasses import dataclass
from typing import Optional, Literal


AudienceType = Literal["household", "farmer", "small_business"]



@dataclass
class LocationResolutionRequest:
    country: str
    user_location: str


@dataclass
class LocationResolutionResponse:
    region_id: str


@dataclass
class RiskQueryRequest:
    region_id: str


@dataclass
class RiskRecord:
    region_id: str
    country: Optional[str]
    adm1_name: Optional[str]
    adm2_name: Optional[str]
    risk_level: str
    valid_at: str
    rainfall_index: Optional[float]
    rainfall_percentile: Optional[float]
    anomaly_mm: Optional[float]
    data_quality: str


@dataclass
class UserProfile:
    audience: AudienceType
    language: str = "en"


@dataclass
class EcoChatRequest:
    location: RiskRecord
    user_profile: UserProfile
    user_question: str
    local_resources: Optional[LocalResourcesResponse] = None


@dataclass
class EcoChatResponse:
    answer: str


@dataclass
class LocalResource:
    name: str
    phone: str
    category: str  # e.g., "Emergency", "Red Cross", "Fire Station", "Shelter"
    country: Optional[str] = None
    region_id: Optional[str] = None
    source: str = "official"  # e.g., "official", "ai_generated"
    is_verified: bool = True


@dataclass
class LocalResourcesResponse:
    emergency_contacts: list[LocalResource]
    shelters: list[LocalResource]
