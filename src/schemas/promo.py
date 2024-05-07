from dataclasses import dataclass, field
from enum import Enum


class PromoStatus(Enum):
    ACTIVE = 'активный'
    INACTIVE = 'неактивный'


@dataclass
class Promo():
    id: int
    name: str
    gift_duration: int
    uses: int
    status: PromoStatus = field(default=PromoStatus.ACTIVE)