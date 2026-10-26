from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.shared.models import ContentItem, User

router = APIRouter()


class ContentItemOut(BaseModel):
    id: int
    mission_id: Optional[int]
    content_type: str
    title: Optional[str]
    body: str
    order: int
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ContentItemCreate(BaseModel):
    mission_id: Optional[int] = None
    content_type: str
    title: Optional[str] = None
    body: str
    order: int = 0


@router.get("/missions/{mission_id}", response_model=List[ContentItemOut])
async def get_mission_content(
    mission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ContentItem)
        .where(ContentItem.mission_id == mission_id, ContentItem.is_published == True)
        .order_by(ContentItem.order)
    )
    return result.scalars().all()


@router.post("/", response_model=ContentItemOut, status_code=status.HTTP_201_CREATED)
async def create_content_item(
    body: ContentItemCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    item = ContentItem(
        mission_id=body.mission_id,
        content_type=body.content_type,
        title=body.title,
        body=body.body,
        order=body.order,
        is_published=False,
        created_by=str(admin.id),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(item)
    await db.flush()
    return item


@router.patch("/{item_id}/publish", response_model=ContentItemOut)
async def publish_content_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    result = await db.execute(select(ContentItem).where(ContentItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conteúdo não encontrado.")
    item.is_published = True
    await db.flush()
    return item
