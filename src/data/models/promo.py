from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models import Base
from src.schemas.promo import PromoStatus


class PromoModel(Base):
    __tablename__ = "promos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    gift_duration: Mapped[int] = mapped_column(Integer)
    uses: Mapped[int] = mapped_column(Integer)
    status: Mapped[PromoStatus] = mapped_column(Enum, default=PromoStatus.ACTIVE)
