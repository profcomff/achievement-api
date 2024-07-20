import logging
from os.path import join as path_join

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_sqlalchemy import db
from pydantic import BaseModel, ConfigDict

from achievement_api.models import Achievement
from achievement_api.settings import get_settings
from achievement_api.utils.image import get_image_dimensions


router = APIRouter(prefix="/achievement", tags=["Achievement"])
logger = logging.getLogger(__name__)
settings = get_settings()


class AchievementGet(BaseModel):
    id: int
    name: str
    description: str
    picture: str | None
    owner_user_id: int

    model_config = ConfigDict(from_attributes=True)


class AchievementCreate(BaseModel):
    name: str
    description: str


class AchievementEdit(BaseModel):
    name: str | None
    description: str | None


@router.get("")
def get_all_achievements() -> list[AchievementGet]:
    return db.session.query(Achievement).filter(Achievement.picture != None).order_by(Achievement.name).all()


@router.get("/{id}")
def get_achievement(id: int) -> AchievementGet:
    return db.session.query(Achievement).get(id)


@router.post("")
def create_achievement(
    new_data: AchievementCreate, user=Depends(UnionAuth(['achievements.achievement.create']))
) -> AchievementGet:
    """Нужны права на: `achievements.achievement.create`"""
    logger.info(f"User id={user['id']} create achievement {new_data.name}")
    achievement = Achievement()
    achievement.name = new_data.name
    achievement.description = new_data.description
    achievement.owner_user_id = user['id']
    db.session.add(achievement)
    db.session.commit()
    return achievement


@router.patch("/{id}")
def edit_achievement(
    id: int, new_data: AchievementEdit, user=Depends(UnionAuth(['achievements.achievement.edit']))
) -> AchievementGet:
    """Нужны права на: `achievements.achievement.edit`"""
    achievement: Achievement = db.session.query(Achievement).get(id)
    logger.info(f"User id={user['id']} edit achievement {new_data.name} ({achievement.name})")
    achievement.name = new_data.name or achievement.name
    achievement.description = new_data.description or achievement.description
    db.session.commit()
    return achievement


@router.patch("/{id}/picture")
async def upload_picture(
    id: int,
    picture_file: UploadFile = File(...),
    user=Depends(UnionAuth(['achievements.achievement.create', 'achievements.achievement.edit'])),
) -> AchievementGet:
    achievement: Achievement = db.session.query(Achievement).get(id)
    logger.info(f"User id={user['id']} uploaded photo for achievement {achievement.name}")
    picture = await picture_file.read()
    await picture_file.close()
    w, h = get_image_dimensions(picture)
    if not (w == h == 512):
        raise HTTPException(400, "Not valid image, should be png 512x512px")
    with open(path_join(settings.STATIC_FOLDER, f"{id}.png"), "wb") as f:
        f.write(picture)
    achievement.picture = f'static/{id}.png'
    db.session.commit()
    return achievement


@router.delete("/{id}", response_model=AchievementGet)
def delete_achievement(id: int, user=Depends(UnionAuth(['achievements.achievement.delete']))) -> AchievementGet:
    """Нужны права на: `achievements.achievement.delete`"""
    achievement: Achievement | None = db.session.get(Achievement, id)
    if not achievement:
        raise HTTPException(404, f"Achievement id={id} not found")
    logger.info(f"User id={user['id']} has deleted achievement {achievement.name}")
    db.session.delete(achievement)
    db.session.commit()
    return achievement
