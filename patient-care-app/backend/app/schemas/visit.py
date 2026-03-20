from pydantic import BaseModel, Field
from typing import Optional


class VisitCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    provider_id: int = Field(..., gt=0)
    visit_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
    chief_complaint: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=5000)
    diagnosis: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field("scheduled", pattern=r"^(scheduled|in_progress|completed|cancelled)$")


class VisitUpdate(BaseModel):
    visit_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
    chief_complaint: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=5000)
    diagnosis: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, pattern=r"^(scheduled|in_progress|completed|cancelled)$")


class VisitResponse(BaseModel):
    id: int
    patient_id: int
    provider_id: int
    visit_date: str
    chief_complaint: Optional[str] = None
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    status: str
    created_at: str
    updated_at: str
