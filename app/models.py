from pydantic import BaseModel
from typing import Dict, List

class ClaimResponse(BaseModel):
    extractedFields: Dict
    missingFields: List[str]
    recommendedRoute: str
    reasoning: str
