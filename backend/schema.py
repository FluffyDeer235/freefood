from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnalysisResult(BaseModel):
    is_event: bool
    has_food: bool
    price: Optional[str] = None
    time: Optional[datetime] = None
    location: Optional[str] = None