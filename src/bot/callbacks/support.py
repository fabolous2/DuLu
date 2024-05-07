from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.states import LetterStatesGroup

router = Router()


@router.callback_query(F.data == 'write_letter')
async def write_letter_handler(
        query: CallbackQuery,
        state: FSMContext,
) -> None:
    pass
