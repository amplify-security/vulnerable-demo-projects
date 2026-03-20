from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
