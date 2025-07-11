import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import User, Campaign
from app.auth import get_password_hash

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
        role="advertiser",
        display_name="Test User",
        contact_email="test@example.com"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="test_creator")
def test_creator_fixture(session: Session):
    creator = User(
        email="creator@example.com",
        hashed_password=get_password_hash("creatorpass"),
        role="creator",
        display_name="Test Creator",
        contact_email="creator@example.com"
    )
    session.add(creator)
    session.commit()
    session.refresh(creator)
    return creator