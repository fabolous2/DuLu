from datetime import datetime, UTC
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

from pytz import timezone


class LetterStatus(Enum):
    WAIT = '⌛На обработке'
    ANSWERED = '🔒Закрыт'


@dataclass
class Letter():
    letter_id: int
    user_id: int
    letter: str
    photos: Dict = field(default=None)
    status: str = field(default="WAIT")
    asked_at: datetime = field(default=datetime.now(timezone('Europe/Moscow')))
    answer: str = field(default=None)
    answered_at: datetime = field(default=datetime.now(timezone('Europe/Moscow')))