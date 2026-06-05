from pydantic import BaseModel
from datetime import datetime


class IncidentCreate(BaseModel):
    service_name: str
    severity: str
    message: str


class IncidentResponse(BaseModel):
    id: int
    service_name: str
    severity: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True