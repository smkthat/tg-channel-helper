from aiogram.fsm.state import StatesGroup, State


class ChannelSG(StatesGroup):
    create_message = State()
    accept_create_message = State()
