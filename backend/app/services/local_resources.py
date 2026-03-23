import json
from pathlib import Path
from typing import List, Optional
from api_models import LocalResource, LocalResourcesResponse
from openrouter_client import generate

# Ground Truth: Verified National Emergency Numbers for Africa
# This ensures that even if AI hallucinations occur, the most critical numbers are always correct.
VERIFIED_NATIONAL_NUMBERS = {
    "NGA": [
        LocalResource(name="Emergency Services", phone="112", category="Emergency", country="NGA", is_verified=True),
        LocalResource(name="Police", phone="199", category="Emergency", country="NGA", is_verified=True),
    ],
    "GHA": [
        LocalResource(name="Police Service", phone="191", category="Emergency", country="GHA", is_verified=True),
        LocalResource(name="Fire Service", phone="192", category="Emergency", country="GHA", is_verified=True),
        LocalResource(name="Ambulance Service", phone="193", category="Emergency", country="GHA", is_verified=True),
    ],
    "KEN": [
        LocalResource(name="Emergency Services", phone="999", category="Emergency", country="KEN", is_verified=True),
    ]
}

def _generate_resources_with_ai(country_iso3: str, region_name: Optional[str] = None) -> List[LocalResource]:
    """
    Uses OpenRouter (LLM) to find likely local resources.
    """
    location_str = f"the country {country_iso3}"
    if region_name:
        location_str = f"the region {region_name} in {country_iso3}"
        
    prompt = (
        f"You are a humanitarian data assistant specializing in disaster preparedness in Africa.\n"
        f"Provide a list of local emergency contacts and flood shelters for {location_str}.\n"
        "Include the name, phone number, and category (Emergency, Red Cross, Fire Station, or Shelter).\n"
        "If you are not 100% sure about a specific phone number or location, DO NOT invent one. "
        "Only provide well-known organizations like the Red Cross or national emergency lines.\n"
        "Respond ONLY with a JSON list of objects matching this structure: "
        '[{"name": "...", "phone": "...", "category": "..."}]'
    )
    
    try:
        raw_response = generate(prompt)
        # Extract JSON from potential markdown blocks
        start = raw_response.find("[")
        end = raw_response.rfind("]")
        if start != -1 and end != -1:
            data = json.loads(raw_response[start:end+1])
            return [
                LocalResource(
                    name=item["name"],
                    phone=item["phone"],
                    category=item["category"],
                    country=country_iso3,
                    source="ai_generated",
                    is_verified=False
                ) for item in data
            ]
    except Exception as e:
        print(f"Error generating resources with AI: {e}")
    return []

def get_resources_for_location(country_iso3: str, region_id: Optional[str] = None, region_name: Optional[str] = None) -> LocalResourcesResponse:
    """
    Returns a list of local emergency contacts and shelters.
    Combines verified national numbers with AI-generated local details.
    """
    # 1. Start with verified national numbers
    resources = VERIFIED_NATIONAL_NUMBERS.get(country_iso3, []).copy()
    
    # 2. Add AI-generated local details (shelters, local chapters)
    ai_resources = _generate_resources_with_ai(country_iso3, region_name)
    resources.extend(ai_resources)
    
    emergency = [r for r in resources if r.category != "Shelter"]
    shelters = [r for r in resources if r.category == "Shelter"]
    
    return LocalResourcesResponse(
        emergency_contacts=emergency,
        shelters=shelters
    )
