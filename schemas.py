from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class IncidentUpdate(BaseModel):
    status: Literal["OPEN", "IN_PROGRESS", "RESOLVED"]

class IncidentOut(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    created_at: datetime
