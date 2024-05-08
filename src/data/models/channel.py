from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base


class ChannelModel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    access_token: Mapped[str] = mapped_column(String, unique=True)
    refresh_token: Mapped[str] = mapped_column(String, unique=True)


