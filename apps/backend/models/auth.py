from pydantic import BaseModel, EmailStr
from typing import Optional

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str
    locale: str = "ja"

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: dict

class UserProfileResponse(BaseModel):
    id: str
    email: str
    display_name: str
    locale: str
    current_plan: Optional[str]
    created_at: str
    updated_at: str

class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = None
    locale: Optional[str] = None
    current_plan: Optional[str] = None