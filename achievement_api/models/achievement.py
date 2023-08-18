from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Achievement(Base):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String)
    description: Mapped[str] = mapped_column(sa.String)
    picture: Mapped[str] = mapped_column(sa.String, nullable=True)
    owner_user_id: Mapped[int] = mapped_column(sa.Integer)
    create_ts: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)
    update_ts: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recievers: Mapped[list[AchievementReciever]] = relationship(back_populates='achievement')


class AchievementReciever(Base):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.Integer)
    achievement_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("achievement.id"))
    create_ts: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)
    update_ts: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    achievement: Mapped[Achievement] = relationship(back_populates='recievers')
