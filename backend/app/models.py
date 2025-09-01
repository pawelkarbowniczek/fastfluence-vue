from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field, Relationship, Column
from pydantic import BaseModel


class UserRole(str, Enum):
    ADVERTISER = "advertiser"
    CREATOR = "creator"


class MediaChannel(str, Enum):
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    YOUTUBE = "YouTube"
    BLOG = "Blog"
    FACEBOOK = "Facebook"
    LINKEDIN = "LinkedIn"
    OTHER = "Other"


class CompensationType(str, Enum):
    CASH = "Cash"
    BARTER = "Barter"
    MIXED = "Mixed"


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PortfolioCampaign(BaseModel):
    title: str
    brand_name: str
    role_in_campaign: str
    landing_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    short_description: str = Field(max_length=280)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole
    display_name: str
    contact_email: str
    phone: Optional[str] = None
    website_url: Optional[str] = None
    social_links: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    portfolio: List[PortfolioCampaign] = Field(default_factory=list, sa_column=Column(JSON))

    # Email activation fields
    is_active: bool = Field(default=False)
    activation_token: Optional[str] = Field(default=None)
    activation_token_expires: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    campaigns: List["Campaign"] = Relationship(back_populates="owner")
    applications: List["Application"] = Relationship(back_populates="creator")


class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
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
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: User = Relationship(back_populates="campaigns")
    applications: List["Application"] = Relationship(back_populates="campaign")


class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    creator_id: int = Field(foreign_key="user.id")
    pitch_text: str
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    campaign: Campaign = Relationship(back_populates="applications")
    creator: User = Relationship(back_populates="applications")