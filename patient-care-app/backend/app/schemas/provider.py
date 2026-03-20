from pydantic import BaseModel, Field
from typing import Optional


class ProviderCreate(BaseModel):
    email: str = Field(..., max_length=255, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    last_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    role: str = Field(..., pattern=r"^(admin|provider|nurse)$")
    specialty: Optional[str] = Field(None, max_length=100)


class ProviderUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Z\s\-']+$")
    specialty: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    role: Optional[str] = Field(None, pattern=r"^(admin|provider|nurse)$")
    is_active: Optional[bool] = None


class ProviderResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    specialty: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str
