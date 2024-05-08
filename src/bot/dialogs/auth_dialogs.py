from aiogram import F
from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Start,
    Row,
    Next, StubScroll, NumberedPager,
    Group, ScrollingGroup, Select, PrevPage, CurrentPage, NextPage
)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia

from src.bot.states import LetterStatesGroup, LetterAnswerSG, WriteMessageSG, LetterHistorySG
from .getters import get_letter, get_wait_letters_db, get_letter_info, get_all_letters_db


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


auth_account_dialog = Dialog(
    Window(

    )
)
