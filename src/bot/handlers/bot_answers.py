import html

from aiogram import Bot, Router, F
from aiogram.types import Message

from dishka import FromDishka

from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.bot.keyboards import inline

router = Router()


@router.message(F.text == '🛖 Главное меню')
async def video_upload_handler(
        message: Message,
) -> None:
    await message.answer(
        text='hi',
        reply_markup=inline.main_kb_markup
    )
