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
from .support_callbacks import (
    confirm_letter,
    sent_photo,
    on_input_photo,
    on_delete_photo,
    on_wait_letters, selected_letter, answer_letter, on_wrote_answer, cancel_letter, on_input_user_id, invalid_user_id,
    on_wrote_message, selected_history_letter, message_input_fixing
)


async def close_dialog(_, __, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.done()


support_dialog = Dialog(
    Window(
        Const("Ваше сообщение будет доставлено администраторам"),
        Start(
            Const('📮Написать'),
            id='write_letter',
            state=LetterStatesGroup.LETTER
        ),
        MessageInput(
            func=message_input_fixing
        ),
        state=LetterStatesGroup.WRITE
    ),
    Window(
        Const("Введите сообщение"),
        TextInput(
            id="letter",
            on_success=Next(),
            filter=F.text.len() >= 10
        ),
        state=LetterStatesGroup.LETTER,
    ),
    Window(
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Format("<blockquote>{letter}</blockquote>"),
        Button(Const("📷Прикрепить скриншот"), id="photo", on_click=sent_photo),
        Button(Const("📨Отправить"), id="send", on_click=confirm_letter),
        Cancel(Const("❌Отменить")),
        state=LetterStatesGroup.SEND,
    ),
    Window(
        Const('Отправьте скриншот'),
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Button(
            Format("🗑️ Delete photo #{media_number}"),
            id="del",
            on_click=on_delete_photo,
            when="media_count",
        ),
        MessageInput(on_input_photo, content_types=[ContentType.PHOTO]),
        Back(Const("⬅️ Назад"), when="photo"),
        state=LetterStatesGroup.SCREEN,
    ),
    getter=get_letter,
)


admin_support_dialog = Dialog(
    Window(
        Const("Выберите действия:"),
        Button(
            Const('⌛ Вопросы в ожидании'),
            id='wait_letter',
            on_click=on_wait_letters
        ),
        Start(
            Const('📜 История вопросов'),
            id='letter_history',
            state=LetterHistorySG.HISTORY
        ),
        Start(
            Const('📨 Написать пользователю'),
            id='write_message',
            state=WriteMessageSG.ENTER_USER_ID
        ),
        MessageInput(
            func=message_input_fixing
        ),
        state=LetterAnswerSG.START
    ),
    Window(
        Const('📪 Список пуст', when=F['is_empty'] == 1),
        Const("⌛Список вопросов, ожидающих ответа:", when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="letter_select",
                items="letters",
                item_id_getter=lambda item: item.letter_id,
                text=Format("№{item.letter_id}"),
                on_click=selected_letter,
                when=F['is_empty'] == 0
            ),
            id="letter_group",
            height=3,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Row(
            PrevPage(
                scroll="letter_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="letter_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="letter_group", text=Format("▶️"),
            ),
            when=F['is_empty'] == 0
        ),
        Back(Format("◀️ В меню")),
        state=LetterAnswerSG.WAIT_LETTERS,
        getter=get_wait_letters_db,
    ),
    Window(
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Multi(
            Format(
                '''
📄 <b>№</b><code>{letter.letter_id}</code>\n
<b>Задан в:</b> {at} (MOSCOW)
<b>user_id</b>: <code>{letter.user_id}</code>
<b>Вопрос от <a href="tg://user?id={letter.user_id}">пользователя</a>:\n</b>
<blockquote>{letter.letter}</blockquote>\n
                '''
            )
        ),
        Button(
            Const('📬 Ответить'),
            id='answer_letter',
            on_click=answer_letter
        ),
        Button(
            Const('❌ Отклонить'),
            id='cancel_letter',
            on_click=cancel_letter
        ),
        Back(Format('◀️ Назад')),
        state=LetterAnswerSG.LETTER_INFO,
        getter=get_letter_info
    ),
    Window(
        Const('🖊️ Напишите ответ пользователю:'),
        TextInput(
            id='write_answer',
            on_success=on_wrote_answer,
        ),
        Back(Format('◀️ Назад')),
        state=LetterAnswerSG.ANSWER,
    ),
    on_process_result=close_dialog,
)


write_message_dialog = Dialog(
    Window(
        Const('👤 Напишите <b>user_id</b> пользователя, которому хотите отправить сообщение'),
        TextInput(
            id='input_id',
            type_factory=int,
            on_success=on_input_user_id,
            on_error=invalid_user_id
        ),
        state=WriteMessageSG.ENTER_USER_ID,
    ),
    Window(
        Const('🖊️ Напишите сообщение пользователю:'),
        MessageInput(on_wrote_message),
        Start(
            Format('◀️ Назад'),
            id='back',
            state=LetterAnswerSG.START
        ),
        state=WriteMessageSG.WRITE,
    ),
    Window(
        Const('❗ Пользователь с таким <b>user_id</b> не был найден...'),
        Start(
            Format('🔁 Попробовать снова'),
            state=WriteMessageSG.ENTER_USER_ID,
            id='try_again'
        ),
        Start(
            Format('◀️ На главную'),
            id='back',
            state=LetterAnswerSG.START
        ),
        state=WriteMessageSG.USER_NOT_FOUND
    ),
    on_process_result=close_dialog
)


letter_history_dialog = Dialog(
    Window(
        Const('📪 Список пуст', when=F['is_empty'] == 1),
        Const("📜 <b>Список всех вопросов, на которые был дан ответ</b>:", when=F['is_empty'] == 0),
        ScrollingGroup(
            Select(
                id="letter_select",
                items="letters",
                item_id_getter=lambda item: item.letter_id,
                text=Format("№{item.letter_id}"),
                on_click=selected_history_letter,
                when=F['is_empty'] == 0
            ),
            id="letter_group",
            height=3,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Row(
            PrevPage(
                scroll="letter_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="letter_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="letter_group", text=Format("▶️"),
            ),
            when=F['is_empty'] == 0
        ),
        Start(
            Format("◀️ В меню"),
            id='to_menu',
            state=LetterAnswerSG.START
        ),
        state=LetterHistorySG.HISTORY,
    ),
    Window(
        DynamicMedia("photo", when="photo"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        Multi(
            Format(
                '''
📄 <b>№</b><code>{letter.letter_id}</code>\n
<b>Задан в:</b> {at} (MOSCOW)
<b>user_id</b>: <code>{letter.user_id}</code>
<b>Вопрос от <a href="tg://user?id={letter.user_id}">пользователя</a>:\n</b>
<blockquote>{letter.letter}</blockquote>\n
<b>Ответ на вопрос:</b>\n <blockquote>{letter.answer}</blockquote>\n
<b>Ответ дан в {answered_at}</b>
                '''
            )
        ),
        Back(Format('◀️ Назад')),
        state=LetterHistorySG.LETTER_INFO,
        getter=get_letter_info
    ),
    Window(
        Const('🖊️ Напишите сообщение пользователю:'),
        TextInput(
            id='write_answer',
            on_success=on_wrote_answer,
        ),
        Back(Format('◀️ Назад')),
        state=LetterHistorySG.SEND_MESSAGE,
    ),
    getter=get_all_letters_db,
)
