from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base
from src.schemas.letter import LetterStatus


class LetterModel(Base):
    __tablename__ = "letters"

    letter_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    letter: Mapped[str] = mapped_column(String)
    photos: Mapped[str] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String, server_default="WAIT")
    asked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    answer: Mapped[str] = mapped_column(String, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


