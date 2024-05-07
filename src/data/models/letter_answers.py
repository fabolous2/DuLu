from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base


class LetterModel(Base):
    __tablename__ = "letter_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    letter_id: Mapped[int] = mapped_column(ForeignKey("letters.letter_id"))
    answer: Mapped[str] = mapped_column(String)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
