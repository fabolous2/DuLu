import html

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Chat
from aiogram_dialog import DialogManager, StartMode, ShowMode

from dishka import FromDishka

from src.bot.states import LetterStatesGroup
from src.services import UserService
from src.main.config import settings
from src.bot.keyboards import inline

router = Router()


@router.callback_query(F.data == 'post_video')
async def post_video_handler(
        query: CallbackQuery,
) -> None:
    pass


@router.callback_query(F.data == 'profile')
async def profile_handler(
        query: CallbackQuery,
        event_chat: Chat,
        bot: Bot,
        user_service: FromDishka[UserService]
) -> None:
    user_id = query.from_user.id
    referral_link = f'{settings.BOT_URL}?start={user_id}'
    user = await user_service.get_user(user_id=user_id)
    referrals = await user_service.user_referrals(user_id=user_id)

    await bot.edit_message_text(
        text=f'''
<b>Ваш профиль <a href="tg://user?id={user_id}">{html.escape(query.from_user.full_name)}</a>:</b>

<b>🎫Статус аккаунта(подписка):</b> {user.status.value}

<b>🔗реферальная ссылка 👇</b> 
<code>{referral_link}</code>
<b>Приглашено:</b> {referrals}

ℹ️(что получит пользователь)
        ''',
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.back_to_menu_kb_markup
    )


# YouTube Studio
@router.callback_query(F.data == 'youtube_studio')
async def youtube_studio_handler(
        query: CallbackQuery,
        bot: Bot,
        event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        text='Добавьте аккаунт',
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.add_account_kb_markup
    )


# TODO: генерация ссылки на аутентификацию и передача ее в inline кнопку (web app)
@router.callback_query(F.data == 'add_account')
async def add_account_handler(
        query: CallbackQuery,
        bot: Bot,
        event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        text='Перейдите по ссылке ниже и дайте доступ нашему приложению',
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=...
    )


# SUPPORT HANDLERS
@router.callback_query(F.data == 'support')
async def support_handler(
        query: CallbackQuery,
        event_chat: Chat,
        bot: Bot,
        dialog_manager: DialogManager
) -> None:
    await bot.edit_message_text(
        text='Нажмите кнопку, чтобы написать сообщение администраторам',
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.write_letter_kb_markup,
    )


@router.callback_query(F.data == 'write_letter')
async def write_letter_handler(
        query: CallbackQuery,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        LetterStatesGroup.LETTER,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND
    )


# MAIN MENU HANDLER
@router.callback_query(F.data.in_(('back_to_menu', 'main_menu')))
async def main_menu_handler(
        query: CallbackQuery,
        event_chat: Chat,
        bot: Bot,
) -> None:
    await bot.edit_message_text(
        text='hi',
        chat_id=event_chat.id,
        message_id=query.message.message_id,
        reply_markup=inline.main_kb_markup
    )


@router.callback_query(F.data == 'download_video')
async def write_letter_handler(
        query: CallbackQuery,
        dialog_manager: DialogManager,
) -> None:
    pass
