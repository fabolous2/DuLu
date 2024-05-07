from typing import Sequence

from src.schemas import Letter
from src.data.dal import SupportDAL


class SupportService:
    def __init__(self, user_dal: SupportDAL) -> None:
        self.support_dal = user_dal

    async def add_letter(self, **kwargs) -> None:
        exists = await self.support_dal.exists(**kwargs)
        if not exists:
            await self.support_dal.add(**kwargs)

    async def get_letter(self, **kwargs) -> Letter:
        letter = await self.support_dal.get_one(**kwargs)
        return letter

    async def get_wait_letters(self) -> Sequence[Letter]:
        letters = await self.support_dal.get_all(status="WAIT")
        return letters

    async def update_letter(self, letter_id: int, **kwargs) -> None:
        await self.support_dal.update(letter_id=letter_id, **kwargs)

    async def get_all_letters(self) -> Sequence[Letter]:
        letters = await self.support_dal.get_absolute_all()
        return letters

    async def get_history_letters(self) -> Sequence[Letter]:
        letters = await self.support_dal.get_history_all()
        return letters
