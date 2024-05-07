from .support_dialogs import support_dialog, admin_support_dialog, write_message_dialog, letter_history_dialog

dialogs = [
    support_dialog,
    admin_support_dialog,
    write_message_dialog,
    letter_history_dialog
]

__all__ = [
    "dialogs"
]
