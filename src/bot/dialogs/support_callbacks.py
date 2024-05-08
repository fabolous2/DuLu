from time import time
import random
from datetime import datetime, UTC

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.common import ManagedScroll

from dishka import FromDishka
from pytz import timezone

from src.bot.dialogs.inject_wrappers import inject_on_click, inject_on_process_result
from src.bot.states import LetterStatesGroup, LetterAnswerSG, WriteMessageSG, LetterHistorySG
from src.services import SupportService, UserService


async def entered_letter(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["letter"] = value
    await dialog_manager.next()


async def sent_photo(
        query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(LetterStatesGroup.SCREEN)


async def on_input_photo(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data.setdefault("photos", []).append(
        (message.photo[-1].file_id, message.photo[-1].file_unique_id),
    )
    await message.delete()
    await dialog_manager.switch_to(LetterStatesGroup.SEND)


async def on_delete_photo(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos", [])
    del photos[media_number]
    if media_number > 0:
        await scroll.set_page(media_number - 1)


@inject_on_click
async def confirm_letter(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    support_service: FromDishka[SupportService]
):
    await callback_query.message.delete()
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    photo_data = dialog_manager.dialog_data
    letter_id = int(time()) + random.randint(1, 99999)
    try:
        letter_widget = dialog_manager.find('letter')
        letter = letter_widget.get_widget_data(dialog_manager, None)
        await support_service.add_letter(
            letter_id=letter_id,
            user_id=callback_query.from_user.id,
            letter=letter,
            photos=photo_data if photo_data else None,
            status="WAIT",
            asked_at=datetime.now(timezone('Europe/Moscow'))
        )
        await callback_query.message.answer(
            f'''
Ваш вопрос <b>№{letter_id}</b> успешно был отправлен администраторам на рассмотрение!
Ожидайте ответа. ⌛
            '''
        )
    except Exception as ex:
        print(ex)
    finally:
        await dialog_manager.done()


async def on_wait_letters(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    try:
        await dialog_manager.switch_to(LetterAnswerSG.WAIT_LETTERS)
    except TypeError as ex:
        print(ex)
        await callback_query.answer("Список вопросов пуст🔐", show_alert=True)


async def selected_letter(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["letter_id"] = item_id
    await dialog_manager.switch_to(LetterAnswerSG.LETTER_INFO)


async def selected_history_letter(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["letter_id"] = item_id
    await dialog_manager.switch_to(LetterHistorySG.LETTER_INFO)


async def answer_letter(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(LetterAnswerSG.ANSWER)


@inject_on_click
async def on_wrote_answer(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    support_service: FromDishka[SupportService]
):
    # dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    answer = value
    letter_info = dialog_manager.dialog_data['letter_info']
    bot = dialog_manager.middleware_data['bot']
    try:
        await bot.send_message(
            chat_id=letter_info.user_id,
            text=f'<b>👨‍🔬 Пришел ответ от администрации на ваш вопрос №{letter_info.letter_id}:</b>'
                 f'\n<blockquote>{answer}</blockquote>'
        )
        await support_service.update_letter(
            letter_id=letter_info.letter_id,
            status='ANSWERED',
            answered_at=datetime.now(timezone('Europe/Moscow')),
            answer=answer
        )
        await message.answer('Вы успешно ответили пользователю!')
    except Exception as ex:
        print(ex)
        await message.answer('Упс... Произошла ошибка при отправке сообщения пользователю(')
    finally:
        await dialog_manager.switch_to(LetterAnswerSG.WAIT_LETTERS)


@inject_on_click
async def cancel_letter(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    support_service: FromDishka[SupportService]
):
    letter_info = dialog_manager.dialog_data['letter_info']
    bot = dialog_manager.middleware_data['bot']
    try:
        await bot.send_message(
            chat_id=letter_info.user_id,
            text=f'😔 К сожалению, ваш вопрос <b>№{letter_info.letter_id}</b> был отклонен администратором.\n'
                 f'Пожалуйста ознакомьтесь с правилами подачи вопроса и попробуйте снова! (снизу будут правила подачи)'
        )
        await support_service.update_letter(
            letter_id=letter_info.letter_id,
            status='CANCELED',
            answered_at=datetime.now(timezone('Europe/Moscow'))
        )
        await callback_query.answer('Вы успешно ответили пользователю!', show_alert=True)
    except Exception as ex:
        print(ex)
        await callback_query.answer('Упс... Произошла ошибка при отправке сообщения пользователю(', show_alert=True)
    finally:
        await dialog_manager.switch_to(LetterAnswerSG.WAIT_LETTERS)


@inject_on_process_result
async def on_input_user_id(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: int,
    user_service: FromDishka[UserService]
):
    is_exists = await user_service.is_registered(user_id=value)
    if is_exists:
        dialog_manager.dialog_data["bot_user_id"] = value
        await dialog_manager.next()
    else:
        await dialog_manager.switch_to(WriteMessageSG.USER_NOT_FOUND)


async def invalid_user_id(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    on_error: ValueError
):
    await message.answer('❗ <b>user_id</b> пользователя введен неверно!')


@inject_on_click
async def on_wrote_message(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    user_id = dialog_manager.dialog_data['bot_user_id']
    bot = dialog_manager.middleware_data['bot']
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f'<b>👨‍🔬 Администратор отправил вам сообщение:</b>'
                 f'\n<blockquote>{message.text}</blockquote>'
        )
        await message.answer('🎉 Сообщение успешно отправлено пользователю!')
    except Exception as ex:
        print(ex)
        await message.answer('Упс... Произошла ошибка при отправке сообщения пользователю(')
    finally:
        await dialog_manager.done()


async def message_input_fixing(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.NO_UPDATE
