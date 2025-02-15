from enum import Enum

from aiogram.filters.callback_data import CallbackData


class AdminCallback(CallbackData, prefix="admin"):
    class Action(str, Enum):
        CHANNEL = 'channel'
        NEWSLETTER = 'newsletter'
        CREATE_MESSAGE = "create_message"
        ACCEPT = 'answer'

    action: Action
    data: str
