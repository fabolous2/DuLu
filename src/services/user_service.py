from src.schemas import User
from src.data.dal import UserDAL


class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self.user_dal = user_dal
    
    async def save_user(self, **kwargs) -> None:
        exists = await self.user_dal.exists(**kwargs)

        if not exists:
            await self.user_dal.add(**kwargs)

    async def get_user(self, **kwargs) -> User:
        user = await self.user_dal.get_one(**kwargs)
        return user

    async def user_referrals(self, **kwargs) -> int:
        count = await self.user_dal.count_referrals(**kwargs)
        return count

    async def is_registered(self, **kwargs) -> bool:
        exists = await self.user_dal.exists(**kwargs)
        return exists
