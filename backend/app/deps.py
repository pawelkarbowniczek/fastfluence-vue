from typing import Annotated, Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from .database import get_session
from .auth import decode_token
from .auth0 import verify_auth0_token, auth0_scheme
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_current_user(
        session: Annotated[Session, Depends(get_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try JWT token first (our own auth system)
    email = decode_token(token)
    if email is not None:
        user = session.exec(select(User).where(User.email == email)).first()
        if user is None:
            raise credentials_exception
        return user

    # If JWT verification fails, try Auth0
    try:
        payload = verify_auth0_token(token)
        auth0_id = payload["sub"]

        user = session.exec(select(User).where(User.auth0_id == auth0_id)).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception


def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user