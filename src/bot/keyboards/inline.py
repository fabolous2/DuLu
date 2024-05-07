from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💾 Загрузить видео', callback_data='post_video')
        ],
        [
            InlineKeyboardButton(text='📊 Творческая студия', callback_data='youtube_studio')
        ],
        [
            InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
        ],
        [
            InlineKeyboardButton(text='📥 Скачать видео', callback_data='download_video')
        ],
        [
            InlineKeyboardButton(text='🪖 Поддержка', callback_data='support')
        ],
    ]
)

back_to_menu_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_menu'),
        ],
    ]
)

write_letter_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📮Написать', callback_data='write_letter')
        ],
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_menu'),
        ],
    ]
)
