from aiogram.enums import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common import ManagedScroll

from dishka.integrations.base import wrap_injection
from dishka import FromDishka

from src.bot.dialogs.inject_wrappers import inject_getter
from src.services import SupportService
from src.schemas import Letter


async def get_letter(dialog_manager: DialogManager, **kwargs):
    letter_widget: TextInput = dialog_manager.find("letter")

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos", [])
    if photos:
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",
            # noqa: E501
            type=ContentType.PHOTO,
        )

    return {
        "letter": letter_widget.get_widget_data(dialog_manager, None),
        "photo": media,
        "media_count": len(photos),
        "media_number": media_number + 1,
    }


@inject_getter
async def get_wait_letters_db(
    dialog_manager: DialogManager,
    support_service: FromDishka[SupportService],
    **kwargs
):
    letters = await support_service.get_wait_letters()
    dialog_manager.dialog_data['letters'] = letters
    return {
        'letters': letters,
        'is_empty': 0 if letters else 1
    }


@inject_getter
async def get_letter_info(
    dialog_manager: DialogManager,
    support_service: FromDishka[SupportService],
    **kwargs
):
    letter_id = dialog_manager.dialog_data["letter_id"]
    letter = await support_service.get_letter(letter_id=letter_id)
    dialog_manager.dialog_data['letter_info'] = letter
    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = letter.photos

    if photos:
        photos = photos['photos']
        dialog_manager.dialog_data.setdefault("photos", letter.photos.values())
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",  # noqa: E501
            type=ContentType.PHOTO,
        )
    return {
        "letter": letter,
        "photo": media,
        "media_count": len(photos) if photos else 0,
        "media_number": media_number + 1,
        "at": letter.asked_at.strftime('%D в %X'),
        "answered_at": letter.answered_at.strftime('%D в %X') if letter.answered_at else "Отсутствует"
    }


@inject_getter
async def get_all_letters_db(
    dialog_manager: DialogManager,
    support_service: FromDishka[SupportService],
    **kwargs
):
    letters = await support_service.get_history_letters()
    dialog_manager.dialog_data['history_letters'] = letters
    return {
        'letters': letters,
        'is_empty': 0 if letters else 1
    }