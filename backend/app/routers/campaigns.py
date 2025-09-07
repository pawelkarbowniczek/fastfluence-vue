from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, or_, and_
from ..database import get_session
from ..deps import get_current_active_user
from ..models import Campaign, User, CompensationType, MediaChannel
from ..schemas import CampaignCreate, CampaignResponse, CampaignUpdate

router = APIRouter()


@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)],
        search: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
        media_channel: Optional[MediaChannel] = Query(None),
        location: Optional[str] = Query(None),
        compensation: Optional[CompensationType] = Query(None),
        min_budget: Optional[int] = Query(None),
        max_budget: Optional[int] = Query(None),
        limit: int = Query(50, le=100),
        offset: int = Query(0, ge=0)
):
    query = select(Campaign).join(User)

    conditions = []

    if search:
        conditions.append(
            or_(
                Campaign.title.contains(search),
                Campaign.description.contains(search)
            )
        )

    if category:
        conditions.append(Campaign.category == category)

    if media_channel:
        conditions.append(Campaign.media_channel == media_channel)

    if location:
        conditions.append(Campaign.location.contains(location))

    if compensation:
        conditions.append(Campaign.compensation == compensation)

    if min_budget is not None:
        conditions.append(Campaign.budget_min >= min_budget)

    if max_budget is not None:
        conditions.append(Campaign.budget_max <= max_budget)

    if conditions:
        query = query.where(and_(*conditions))

    campaigns = session.exec(query.offset(offset).limit(limit)).all()

    # Manually load owner relationship
    for campaign in campaigns:
        if not hasattr(campaign, 'owner') or campaign.owner is None:
            campaign.owner = session.get(User, campaign.owner_id)

    return campaigns


@router.post("/", response_model=CampaignResponse)
def create_campaign(
        campaign_data: CampaignCreate,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role != "advertiser":
        raise HTTPException(status_code=403, detail="Tylko reklamodawcy mogą tworzyć kampanie")

    # Validate budget requirements
    if campaign_data.compensation in [CompensationType.CASH, CompensationType.MIXED]:
        if campaign_data.budget_min is None or campaign_data.budget_max is None:
            raise HTTPException(
                status_code=400,
                detail="Budżet min i max są wymagane dla płatnych kampanii"
            )

    if campaign_data.compensation in [CompensationType.BARTER, CompensationType.MIXED]:
        if not campaign_data.barter_descr:
            raise HTTPException(
                status_code=400,
                detail="Opis barteru jest wymagany dla kampanii barterowych"
            )

    db_campaign = Campaign(
        owner_id=current_user.id,
        **campaign_data.model_dump()
    )
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)

    # Load owner relationship
    db_campaign.owner = session.get(User, db_campaign.owner_id)

    return db_campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
        campaign_id: int,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    campaign = session.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Kampania nie została znaleziona")

    # Load owner relationship
    campaign.owner = session.get(User, campaign.owner_id)
    if not campaign.owner:
        raise HTTPException(status_code=404, detail="Właściciel kampanii nie został znaleziony")

    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
        campaign_id: int,
        campaign_data: CampaignUpdate,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    campaign = session.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Kampania nie została znaleziona")

    if campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień do edycji tej kampanii")

    campaign_dict = campaign_data.model_dump(exclude_unset=True)
    for field, value in campaign_dict.items():
        setattr(campaign, field, value)

    session.add(campaign)
    session.commit()
    session.refresh(campaign)

    # Load owner relationship
    campaign.owner = session.get(User, campaign.owner_id)

    return campaign


@router.delete("/{campaign_id}")
def delete_campaign(
        campaign_id: int,
        session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    campaign = session.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Kampania nie została znaleziona")

    if campaign.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak uprawnień do usunięcia tej kampanii")

    session.delete(campaign)
    session.commit()
    return {"message": "Kampania została usunięta"}