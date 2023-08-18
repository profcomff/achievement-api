import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from pydantic import BaseModel, ConfigDict

from achievement_api.settings import get_settings
from achievement_api.models import Achievement


router = APIRouter(prefix="/achievement", tags=["Achievement"])
logger = logging.getLogger(__name__)
settings = get_settings()


class RecieverGet(BaseModel):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class AchievementGet(BaseModel):
    id: int
    name: str
    description: str
    picture: str | None
    owner_user_id: int
    recievers: list[RecieverGet]

    model_config = ConfigDict(from_attributes=True)


class AchievementCreate(BaseModel):
    name: str
    description: str


class AchievementEdit(BaseModel):
    name: str | None
    description: str | None


@router.get("")
def get_all_achievements() -> list[AchievementGet]:
    return db.session.query(Achievement).order_by(Achievement.name).all()


@router.get("/{id}")
def get_achievement(id: int) -> AchievementGet:
    return db.session.query(Achievement).get(id)


@router.post("")
def create_achievement(new_data: AchievementCreate, user=Depends(UnionAuth(['achievements.achievement.create']))) -> AchievementGet:
    """Нужны права на: `achievements.achievement.create`"""
    achievement = Achievement()
    achievement.name = new_data.name
    achievement.description = new_data.description
    achievement.owner_user_id = user['id']
    db.session.add(achievement)
    db.session.commit()
    return achievement


@router.patch("/{id}")
def edit_achievement(id: int, new_data: AchievementEdit, user=Depends(UnionAuth(['achievements.achievement.edit']))) -> AchievementGet:
    """Нужны права на: `achievements.achievement.edit`"""
    achievement: Achievement = db.session.query(Achievement).get(id)
    achievement.name = new_data.name or achievement.name
    achievement.description = new_data.description or achievement.description
    return achievement
