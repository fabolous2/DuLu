from aiogram.fsm.state import State, StatesGroup


class LetterStatesGroup(StatesGroup):
    WRITE = State()
    LETTER = State()
    SCREEN = State()
    SEND = State()


class LetterAnswerSG(StatesGroup):
    START = State()
    WAIT_LETTERS = State()
    LETTER_INFO = State()
    ANSWERED_LETTERS = State()
    ANSWER = State()


class WriteMessageSG(StatesGroup):
    ENTER_USER_ID = State()
    WRITE = State()
    SUCCESSFULLY_SENT = State()
    USER_NOT_FOUND = State()


class LetterHistorySG(StatesGroup):
    HISTORY = State()
    LETTER_INFO = State()
    SEND_MESSAGE = State()