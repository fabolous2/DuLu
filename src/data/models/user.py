from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base
from src.schemas.user import UserStatus


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referral_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.BASIC)
    limit: Mapped[int] = mapped_column(Integer, default=2)
    language: Mapped[str] = mapped_column(String)

