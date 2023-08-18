import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel, ConfigDict

from achievement_api.models import Achievement, AchievementReciever
from achievement_api.settings import get_settings


router = APIRouter(prefix="/achievement/{achievement_id}/reciever", tags=["Reciever"])
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


@router.get("")
def get_all_recievers(achievement_id: int) -> AchievementGet:
    return db.session.query(Achievement).get(achievement_id)


@router.post("/{user_id}")
def create_reciever(
    achievement_id: int, user_id: int, reciever=Depends(UnionAuth(['achievements.achievement.give']))
) -> AchievementGet:
    """Нужны права на: `achievements.achievement.give`"""
    achievement: Achievement = db.session.query(Achievement).get(achievement_id)
    reciever: AchievementReciever = (
        db.session.query(AchievementReciever)
        .where(AchievementReciever.user_id == user_id)
        .where(AchievementReciever.achievement_id == achievement_id)
        .one_or_none()
    )
    if reciever:
        raise HTTPException(400, f"User id={user_id} already has id={achievement_id}")
    reciever = AchievementReciever()
    reciever.user_id = user_id
    achievement.recievers.append(reciever)
    db.session.commit()
    return achievement


@router.delete("/{user_id}")
def revoke_reciever(
    achievement_id: int, user_id: int, user=Depends(UnionAuth(['achievements.achievement.revoke']))
) -> AchievementGet:
    """Нужны права на: `achievements.achievement.revoke`"""
    achievement = db.session.query(Achievement).get(achievement_id)
    reciever: AchievementReciever = (
        db.session.query(AchievementReciever)
        .where(AchievementReciever.user_id == user_id)
        .where(AchievementReciever.achievement_id == achievement_id)
        .one_or_none()
    )
    if reciever:
        db.session.delete(reciever)
        db.session.commit()
        return achievement
    raise HTTPException(400, f"No such user id={user_id} with achivement id={achievement_id} found")
