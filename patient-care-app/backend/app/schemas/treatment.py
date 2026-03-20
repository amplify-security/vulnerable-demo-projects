from pydantic import BaseModel, Field
from typing import Optional


class TreatmentCreate(BaseModel):
    visit_id: int = Field(..., gt=0)
    treatment_type: str = Field(..., pattern=r"^(medication|procedure)$")
    name: str = Field(..., min_length=1, max_length=200)
    dosage: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field("active", pattern=r"^(active|completed|discontinued)$")


class TreatmentUpdate(BaseModel):
    treatment_type: Optional[str] = Field(None, pattern=r"^(medication|procedure)$")
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    dosage: Optional[str] = Field(None, max_length=100)
    frequency: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, pattern=r"^(active|completed|discontinued)$")


class TreatmentResponse(BaseModel):
    id: int
    visit_id: int
    treatment_type: str
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    notes: Optional[str] = None
    status: str
    created_at: str
    updated_at: str
