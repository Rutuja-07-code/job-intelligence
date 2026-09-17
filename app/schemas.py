from pydantic import BaseModel
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None
class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None = None
    created_at: datetime
class CompanyUpdate(BaseModel):
    name: str
    website: str | None = None
class JobCreate(BaseModel):
    title: str
    description: str | None = None
    location: str | None = None
class JobResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str | None
    location: str | None
    created_at: datetime
class JobWithCompanyResponse(BaseModel):
    id: int
    title: str
    description: str | None
    location: str | None
    company_id: int
    company_name: str
class UserCreate(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
class UserLogin(BaseModel):
    email: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str