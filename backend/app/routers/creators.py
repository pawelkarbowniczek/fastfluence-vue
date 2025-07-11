from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_, and_
from ..database import get_session
from ..deps import get_current_active_user
from ..models import User, UserRole, MediaChannel
from ..schemas import UserPublic

router = APIRouter()

@router.get("/", response_model=List[UserPublic])
def get_creators(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    media_channel: Optional[MediaChannel] = Query(None),
    location: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    query = select(User).where(User.role == UserRole.CREATOR)
    
    conditions = []
    
    if search:
        conditions.append(
            or_(
                User.display_name.contains(search),
                User.contact_email.contains(search)
            )
        )
    
    # Note: For portfolio-based filtering, we'd need to implement JSON queries
    # which vary by database. This is a simplified version.
    
    if conditions:
        query = query.where(and_(*conditions))
    
    creators = session.exec(query.offset(offset).limit(limit)).all()
    return creators