from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None


class CompanyResponse(ORMResponse):
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


class JobResponse(ORMResponse):
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


class JobImportRequest(BaseModel):
    keyword: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=100)
    results_per_page: int = Field(default=10, ge=1, le=50)


class JobImportResponse(BaseModel):
    fetched: int
    imported: int
    skipped: int


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(ORMResponse):
    id: int
    email: str
    created_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProfileCreate(BaseModel):
    full_name: str


class ProfileResponse(ORMResponse):
    id: int
    user_id: int
    full_name: str
    created_at: datetime


class SkillCreate(BaseModel):
    name: str


class JobRequirementCreate(BaseModel):
    skill_name: str


class JobRequirementResponse(ORMResponse):
    id: int
    job_id: int
    skill_name: str


class JobRecommendationResponse(BaseModel):
    job_id: int
    job_title: str
    company_name: str
    location: str | None
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
