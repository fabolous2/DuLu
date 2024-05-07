from datetime import datetime

from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from dishka import FromDishka

from aiogram_dialog import DialogManager, StartMode, ShowMode

from pytz import timezone

from src.services import UserService
from src.bot.keyboards import reply, inline
from src.bot.states import LetterAnswerSG

router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
    user_service: FromDishka[UserService]
) -> None:
    user_id = message.from_user.id
    is_registered = await user_service.is_registered(user_id=user_id)

    if not is_registered:
        now = datetime.now(timezone('Europe/Moscow'))
        await user_service.save_user(
            user_id=user_id,
            created_at=now,
            last_activity=now,
            language=message.from_user.language_code
        )
    await message.answer("bot introduction", reply_markup=reply.main_kb_markup)
    await message.answer("Hi", reply_markup=inline.main_kb_markup)


@router.message(Command('support'))
async def support_handler(
    message: Message,
    dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        LetterAnswerSG.START,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND
    )
