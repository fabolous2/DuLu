from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from dataclasses import dataclass, field


class UserStatus(Enum):
    BASIC = 'basic'
    PRO = 'pro'


@dataclass
class User():
    user_id: int 
    referral_id: Optional[int]
    last_activity: datetime
    language: str
    status: UserStatus = field(default=UserStatus.BASIC)
    limit: int = field(default=2)
    created_at: datetime = field(default=datetime.now(UTC))