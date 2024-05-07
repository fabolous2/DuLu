from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🛖 Главное меню'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)
