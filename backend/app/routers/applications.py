from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..database import get_session
from ..deps import get_current_active_user
from ..models import Application, Campaign, User, ApplicationStatus
from ..schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ApplicationResponse)
def create_application(
        application_data: ApplicationCreate,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role != "creator":
        raise HTTPException(
            status_code=403,
            detail="Tylko twórcy mogą aplikować na kampanie"
        )

    # Check if campaign exists
    campaign = session.get(Campaign, application_data.campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Kampania nie została znaleziona"
        )

    # Check if user already applied to this campaign
    existing_application = session.exec(
        select(Application).where(
            Application.campaign_id == application_data.campaign_id,
            Application.creator_id == current_user.id
        )
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Już aplikowałeś na tę kampanię"
        )

    # Check if user is not applying to their own campaign
    if campaign.owner_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Nie możesz aplikować na własną kampanię"
        )

    # Create application
    db_application = Application(
        campaign_id=application_data.campaign_id,
        creator_id=current_user.id,
        pitch_text=application_data.pitch_text,
        proposed_price=application_data.proposed_price
    )

    session.add(db_application)
    session.commit()
    session.refresh(db_application)

    # Load relationships
    db_application.campaign = session.get(Campaign, db_application.campaign_id)
    db_application.creator = session.get(User, db_application.creator_id)
    if db_application.campaign:
        db_application.campaign.owner = session.get(User, db_application.campaign.owner_id)

    return db_application


@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)],
        campaign_id: Optional[int] = None,
        status: Optional[ApplicationStatus] = None
):
    query = select(Application)

    # Filter based on user role
    if current_user.role == "advertiser":
        # Show applications for campaigns owned by this advertiser
        query = query.join(Campaign).where(Campaign.owner_id == current_user.id)
    else:
        # Show applications created by this creator
        query = query.where(Application.creator_id == current_user.id)

    # Additional filters
    if campaign_id:
        query = query.where(Application.campaign_id == campaign_id)

    if status:
        query = query.where(Application.status == status)

    applications = session.exec(query).all()

    # Load relationships
    for application in applications:
        if not application.campaign:
            application.campaign = session.get(Campaign, application.campaign_id)
        if not application.creator:
            application.creator = session.get(User, application.creator_id)
        if application.campaign and not hasattr(application.campaign, 'owner'):
            application.campaign.owner = session.get(User, application.campaign.owner_id)

    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
        application_id: int,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Aplikacja nie została znaleziona")

    # Load relationships
    if not application.campaign:
        application.campaign = session.get(Campaign, application.campaign_id)
    if not application.creator:
        application.creator = session.get(User, application.creator_id)
    if application.campaign and not hasattr(application.campaign, 'owner'):
        application.campaign.owner = session.get(User, application.campaign.owner_id)

    # Check permissions
    if current_user.role == "creator" and application.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    elif current_user.role == "advertiser" and application.campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
        application_id: int,
        application_data: ApplicationUpdate,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Aplikacja nie została znaleziona")

    # Load campaign relationship
    if not application.campaign:
        application.campaign = session.get(Campaign, application.campaign_id)

    # Only campaign owner can update application status
    if application.campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    if application_data.status:
        application.status = application_data.status

    session.add(application)
    session.commit()
    session.refresh(application)

    # Load relationships for response
    if not application.creator:
        application.creator = session.get(User, application.creator_id)
    if application.campaign and not hasattr(application.campaign, 'owner'):
        application.campaign.owner = session.get(User, application.campaign.owner_id)

    return application


@router.delete("/{application_id}")
def delete_application(
        application_id: int,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Aplikacja nie została znaleziona")

    # Only creator who created the application can delete it
    if application.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    # Can only delete pending applications
    if application.status != ApplicationStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Można usunąć tylko oczekujące aplikacje"
        )

    session.delete(application)
    session.commit()
    return {"message": "Aplikacja została usunięta"}