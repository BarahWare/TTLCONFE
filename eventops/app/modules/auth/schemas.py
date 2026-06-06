from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    org_id: int | None = None

    model_config = {"from_attributes": True}


class UpdateMeRequest(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
