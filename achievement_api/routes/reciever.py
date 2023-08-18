import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends

from achievement_api.settings import get_settings


router = APIRouter(prefix="/achievement/{achievement_id}/reciever", tags=["Reciever"])
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("")
def get_all_recievers(achievement_id: int):
    pass


@router.post("/{user_id}")
def create_reciever(achievement_id: int, user_id: int, user=Depends(UnionAuth(['achievements.achievement.give']))):
    """Нужны права на: `achievements.achievement.give`"""
    pass


@router.delete("/{user_id}")
def revoke_reciever(achievement_id: int, user_id: int, user=Depends(UnionAuth(['achievements.achievement.revoke']))):
    """Нужны права на: `achievements.achievement.revoke`"""
    pass
