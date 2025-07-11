from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..deps import get_current_active_user
from ..models import User
from ..schemas import UserResponse, UserUpdate, UserPublic

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    user_dict = user_data.model_dump(exclude_unset=True)
    for field, value in user_dict.items():
        setattr(current_user, field, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserPublic)
def get_user_profile(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie został znaleziony")
    
    # Hide phone from same-side viewers
    user_public = UserPublic.model_validate(user)
    return user_public