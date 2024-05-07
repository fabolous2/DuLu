from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base


class VideoModel(Base):
    __tablename__ = "videos"

    video_id: Mapped[str] = mapped_column(String, primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.channel_id"), unique=True)
