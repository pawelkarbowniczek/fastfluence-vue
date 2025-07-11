from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .models import UserRole, MediaChannel, CompensationType, ApplicationStatus, PortfolioCampaign

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    display_name: str
    contact_email: EmailStr
    phone: Optional[str] = None
    website_url: Optional[str] = None
    social_links: List[str] = []
    portfolio: List[PortfolioCampaign] = []

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    social_links: Optional[List[str]] = None
    portfolio: Optional[List[PortfolioCampaign]] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

class UserPublic(BaseModel):
    id: int
    display_name: str
    contact_email: EmailStr
    website_url: Optional[str] = None
    social_links: List[str] = []
    portfolio: List[PortfolioCampaign] = []

class CampaignBase(BaseModel):
    title: str
    description: str
    category: str
    media_channel: MediaChannel
    location: str
    compensation: CompensationType
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    barter_descr: Optional[str] = None
    deadline: datetime

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    media_channel: Optional[MediaChannel] = None
    location: Optional[str] = None
    compensation: Optional[CompensationType] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    barter_descr: Optional[str] = None
    deadline: Optional[datetime] = None

class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserPublic

class ApplicationBase(BaseModel):
    pitch_text: str

class ApplicationCreate(ApplicationBase):
    campaign_id: int

class ApplicationResponse(ApplicationBase):
    id: int
    campaign_id: int
    creator_id: int
    status: ApplicationStatus
    created_at: datetime
    campaign: CampaignResponse
    creator: UserPublic