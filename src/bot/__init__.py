from .handlers import commands, bot_answers
from .callbacks import callback

routers = [
    commands.router,
    bot_answers.router,
    callback.router
]

__all__ = [
    'routers'
]