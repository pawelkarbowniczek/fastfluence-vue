from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..database import get_session
from ..auth import authenticate_user, create_access_token, get_password_hash
from ..auth0 import get_current_user_auth0
from ..models import User
from ..schemas import Token, UserCreate, UserResponse, Auth0LoginRequest
from ..config import settings
from ..email import generate_activation_token, send_activation_email, send_welcome_email

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
        user_data: UserCreate,
        session: Annotated[Session, Depends(get_session)]
):
    db_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email już jest zarejestrowany"
        )

    # Generate activation token
    activation_token = generate_activation_token()
    activation_expires = datetime.utcnow() + timedelta(hours=settings.ACTIVATION_TOKEN_EXPIRE_HOURS)

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        display_name=user_data.display_name,
        contact_email=user_data.contact_email,
        phone=user_data.phone,
        website_url=user_data.website_url,
        social_links=user_data.social_links,
        portfolio=user_data.portfolio,
        is_active=False,  # User needs to activate account
        activation_token=activation_token,
        activation_token_expires=activation_expires
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Send activation email
    email_sent = send_activation_email(db_user, activation_token)
    if not email_sent:
        # Log error but don't fail registration
        print(f"Failed to send activation email to {db_user.email}")

    return db_user


@router.post("/activate/{token}")
def activate_account(
        token: str,
        session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(
        select(User).where(
            User.activation_token == token,
            User.activation_token_expires > datetime.utcnow(),
            User.is_active == False
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token aktywacyjny jest nieprawidłowy lub wygasł"
        )

    # Activate account
    user.is_active = True
    user.activation_token = None
    user.activation_token_expires = None
    session.add(user)
    session.commit()

    # Send welcome email
    send_welcome_email(user)

    return {"message": "Konto zostało pomyślnie aktywowane"}


@router.post("/resend-activation")
def resend_activation(
        email: str,
        session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(
        select(User).where(
            User.email == email,
            User.is_active == False
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Użytkownik nie został znaleziony lub konto jest już aktywne"
        )

    # Generate new activation token
    activation_token = generate_activation_token()
    activation_expires = datetime.utcnow() + timedelta(hours=settings.ACTIVATION_TOKEN_EXPIRE_HOURS)

    user.activation_token = activation_token
    user.activation_token_expires = activation_expires
    session.add(user)
    session.commit()

    # Send new activation email
    email_sent = send_activation_email(user, activation_token)
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Błąd wysyłania emaila aktywacyjnego"
        )

    return {"message": "Email aktywacyjny został wysłany ponownie"}


@router.post("/token", response_model=Token)
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[Session, Depends(get_session)]
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy email lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if account is activated
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Konto nie zostało jeszcze aktywowane. Sprawdź swoją skrzynkę email.",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth0/token", response_model=Token)
def auth0_login(
        auth0_data: Auth0LoginRequest,
        session: Annotated[Session, Depends(get_session)]
):
    # Check if user with this Auth0 ID exists
    user = session.exec(
        select(User).where(User.auth0_id == auth0_data.auth0_id)
    ).first()

    # If user doesn't exist, create a new one
    if not user:
        # Check if email already exists
        email_user = session.exec(
            select(User).where(User.email == auth0_data.email)
        ).first()

        if email_user:
            # Link Auth0 account with existing user
            email_user.auth0_id = auth0_data.auth0_id
            email_user.is_active = True  # Auth0 users are verified
            session.add(email_user)
            session.commit()
            session.refresh(email_user)
            user = email_user
        else:
            # Create new user
            user = User(
                email=auth0_data.email,
                hashed_password="",  # Not used with Auth0
                role=auth0_data.role,
                display_name=auth0_data.display_name or auth0_data.email.split('@')[0],
                contact_email=auth0_data.email,
                auth0_id=auth0_data.auth0_id,
                is_active=True  # Auth0 users are verified
            )
            session.add(user)
            session.commit()
            session.refresh(user)

    # Create a token for the user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth0/info")
def auth0_info():
    """Return Auth0 configuration for the frontend"""
    return {
        "domain": settings.AUTH0_DOMAIN,
        "client_id": settings.AUTH0_CLIENT_ID,
        "audience": settings.AUTH0_API_AUDIENCE,
        "callback_url": settings.AUTH0_CALLBACK_URL
    }