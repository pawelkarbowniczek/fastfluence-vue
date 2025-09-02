import json
from urllib.request import urlopen
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from .config import settings
from .database import get_session
from .models import User, UserRole

# Auth0 Config
AUTH0_DOMAIN = settings.AUTH0_DOMAIN
API_AUDIENCE = settings.AUTH0_API_AUDIENCE
ALGORITHMS = ["RS256"]

# HTTPBearer for token extraction
http_bearer = HTTPBearer()


class Auth0HTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Auth0HTTPBearer, self).__init__(auto_error=auto_error)


auth0_scheme = Auth0HTTPBearer()


# Helper to fetch Auth0 public key
def get_auth0_public_key():
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    return jwks


# Verify and decode Auth0 token
def verify_auth0_token(token):
    # Get the Auth0 public key
    jwks = get_auth0_public_key()

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose our key
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:
        try:
            # Validate the token using PyJWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid claims, please check the audience and issuer",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to parse authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to find appropriate key",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Dependency to get the current user from Auth0 token
async def get_current_user_auth0(
        credentials: HTTPAuthorizationCredentials = Depends(auth0_scheme),
        session: Session = Depends(get_session),
):
    token = credentials.credentials
    payload = verify_auth0_token(token)

    # Extract user info from Auth0 payload
    auth0_id = payload["sub"]
    email = payload.get("email", "")

    # Check if user exists in our database
    user = session.exec(select(User).where(User.auth0_id == auth0_id)).first()

    if not user:
        # If the user doesn't exist, create a new one based on Auth0 info
        # Note: In a real application, you might want to collect additional information
        user = User(
            email=email,
            auth0_id=auth0_id,
            hashed_password="",  # Not used with Auth0
            display_name=payload.get("name", email.split("@")[0]),
            contact_email=email,
            role=UserRole.CREATOR,  # Default role
            is_active=True,  # Auth0 users are active by default
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    return user