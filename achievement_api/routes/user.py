import logging

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from pydantic import BaseModel, ConfigDict

from achievement_api.models import Achievement, AchievementReciever
from achievement_api.settings import get_settings


router = APIRouter(prefix="/user", tags=["User"])
logger = logging.getLogger(__name__)
settings = get_settings()


class AchievementGet(BaseModel):
    id: int
    name: str
    description: str
    picture: str | None
    owner_user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserGet(BaseModel):
    user_id: int
    achievement: list[AchievementGet]

    model_config = ConfigDict(from_attributes=True)


@router.get("/{user_id}")
def get_all_achievements(user_id: int) -> UserGet:
    achievements = (
        db.session.query(Achievement).join(AchievementReciever).where(AchievementReciever.user_id == user_id).all()
    )
    return UserGet(user_id=user_id, achievement=achievements)
