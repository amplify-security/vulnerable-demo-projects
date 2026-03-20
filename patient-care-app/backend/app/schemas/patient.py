from pydantic import BaseModel, Field
from typing import Optional


class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    last_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    date_of_birth: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    gender: Optional[str] = Field(None, pattern=r"^(male|female|other|unknown)$")
    phone: Optional[str] = Field(None, max_length=20, pattern=r"^[\d\s\-\+\(\)]+$")
    email: Optional[str] = Field(None, max_length=255, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    address: Optional[str] = Field(None, max_length=500)
    emergency_contact: Optional[str] = Field(None, max_length=500)


class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    date_of_birth: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    gender: Optional[str] = Field(None, pattern=r"^(male|female|other|unknown)$")
    phone: Optional[str] = Field(None, max_length=20, pattern=r"^[\d\s\-\+\(\)]+$")
    email: Optional[str] = Field(None, max_length=255, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    address: Optional[str] = Field(None, max_length=500)
    emergency_contact: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class PatientResponse(BaseModel):
    id: int
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str
