from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schemas import Letter
from src.data.models import LetterModel


class SupportDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(LetterModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, letter_id: int, **kwargs) -> None:
        query = update(LetterModel).where(LetterModel.letter_id == letter_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(LetterModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(LetterModel, key)
                )
            )
        )
        result = await self.session.execute(query)

        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        # Проверка существования пользователя
        letter_exists = await self.exists(user_id=user_id)

        if not letter_exists:
            return False  # Пользователь не существует, колонка не заполнена

        query = select(
            *(
                getattr(LetterModel, column_name)
                for column_name in column_names
                if hasattr(LetterModel, column_name)
            )
        ).where(LetterModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()

        return column_value is not None

    async def _get(self, **kwargs) -> Result[tuple[LetterModel]] | None:
        exists = await self.exists(**kwargs)

        if not exists:
            return None

        query = select(LetterModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs) -> Letter | None:
        res = await self._get(**kwargs)

        if res:
            db_letter = res.scalar_one_or_none()
            return Letter(
                letter_id=db_letter.letter_id,
                user_id=db_letter.user_id,
                letter=db_letter.letter,
                photos=db_letter.photos,
                status=db_letter.status,
                asked_at=db_letter.asked_at,
                answered_at=db_letter.answered_at,
                answer=db_letter.answer
            )

    async def get_all(self, **kwargs) -> list[Letter] | None:
        res = await self._get(**kwargs)

        if res:
            db_letters = res.scalars().all()
            return [
                Letter(
                    letter_id=db_letter.letter_id,
                    user_id=db_letter.user_id,
                    letter=db_letter.letter,
                    photos=db_letter.photos,
                    status=db_letter.status,
                    asked_at=db_letter.asked_at,
                    answered_at=db_letter.answered_at,
                    answer=db_letter.answer
                )
                for db_letter in db_letters
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(LetterModel).filter_by(**kwargs)

        await self.session.execute(query)
        await self.session.commit()

    async def get_absolute_all(self) -> list[Letter]:
        query = select(LetterModel)
        result = await self.session.execute(query)
        db_letters = result.scalars().all()

        return [
            Letter(
                letter_id=db_letter.letter_id,
                user_id=db_letter.user_id,
                letter=db_letter.letter,
                photos=db_letter.photos,
                status=db_letter.status,
                asked_at=db_letter.asked_at,
                answered_at=db_letter.answered_at,
                answer=db_letter.answer
            )
            for db_letter in db_letters
        ]

    async def get_history_all(self) -> list[Letter]:
        query = select(LetterModel).where(LetterModel.status.in_(('ANSWERED', 'CANCELED')))
        result = await self.session.execute(query)
        db_letters = result.scalars().all()

        return [
            Letter(
                letter_id=db_letter.letter_id,
                user_id=db_letter.user_id,
                letter=db_letter.letter,
                photos=db_letter.photos,
                status=db_letter.status,
                asked_at=db_letter.asked_at,
                answered_at=db_letter.answered_at,
                answer=db_letter.answer
            )
            for db_letter in db_letters
        ]

