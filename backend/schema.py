from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnalysisResult(BaseModel):
    has_food: bool
    is_free: bool
