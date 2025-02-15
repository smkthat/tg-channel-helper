import asyncio
from typing import Union

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ChatAction, ChatType, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.configuration.log import get_logger
from app.halpers.utils import delete_or_edit_message, delete_ui_messages
from app.handlers.callbacks.callback import AdminCallback
from app.handlers.filters.filter import AdminChatFilter
from app.keyboards.keyboard import (
    get_admin_start_keyboard,
    get_channel_keyboard,
    get_keyboard_from_data
)

LOGGER = get_logger(__name__, '../../logs')


async def start(m: Message, bot: Bot, state: FSMContext, dynamic_data: dict):
    await state.clear()
    await delete_menu(m, bot, state)
    start_text = dynamic_data['start_message']['text']
    menu = await m.answer(
        text=start_text.format(user_mention=m.from_user.mention_markdown()),
        reply_markup=get_keyboard_from_data(buttons_data=dynamic_data['start_message'].get('buttons', [[]]))
    )
    await state.update_data(menu_id=menu.message_id)
    await bot.send_chat_action(
        chat_id=m.chat.id,
        action=ChatAction.TYPING
    )
    if dynamic_data['start_message'].get('after', None):
        await asyncio.sleep(delay=dynamic_data['start_message']['after'][-1]['ttl'])
        await m.answer(text=dynamic_data['start_message']['after'][-1]['text'])


async def start_admin(m: Message, bot: Bot, state: FSMContext):
    if state_data := await state.get_data():
        if tmp_message_id := state_data.get('tmp_message_id'):
            await delete_or_edit_message(chat_id=m.chat.id, message_id=tmp_message_id, bot=bot)

        await delete_or_edit_message(chat_id=m.chat.id, message_id=m.message_id, bot=bot)
        await delete_ui_messages(bot=bot, state=state)

    await delete_menu(m, bot, state)
    await state.clear()

    menu = await m.answer(
        text=f'👋🏽 {m.from_user.mention_markdown()}, приветствуем Вас!'
             '\n\nВыберите интересующий Вас раздел 👇🏽',
        reply_markup=get_admin_start_keyboard()
    )
    await state.update_data(menu_id=menu.message_id)


async def start_admin_call(c: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await delete_menu(c, bot, state)
    menu = await c.message.answer(
        text=f'👋🏽 {c.from_user.mention_markdown()}, приветствуем Вас!'
             '\n\nВыберите интересующий Вас раздел 👇🏽',
        reply_markup=get_admin_start_keyboard()
    )
    await state.update_data(menu_id=menu.message_id)


async def delete_menu(message_or_call: Union[Message, CallbackQuery], bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    if menu_id := state_data.get('menu_id'):
        await delete_or_edit_message(chat_id=message_or_call.chat.id, message_id=menu_id, bot=bot)


async def channel(c: CallbackQuery):
    await c.message.edit_reply_markup(
        reply_markup=get_channel_keyboard()
    )


async def delete_pinned_message(m: Message):
    await m.delete()


def register_main_handlers(dp: Dispatcher):
    dp.message.register(
        delete_pinned_message,
        lambda message: message.chat.type == ChatType.PRIVATE,
        F.content_type == ContentType.PINNED_MESSAGE
    )
    dp.message.register(
        start_admin,
        Command(commands='start'),
        AdminChatFilter(),
        lambda message: message.chat.type == ChatType.PRIVATE
    )
    dp.message.register(
        start,
        Command(commands='start'),
        lambda message: message.chat.type == ChatType.PRIVATE
    )
    dp.callback_query.register(
        channel,
        AdminCallback.filter(F.action == AdminCallback.Action.CHANNEL),
        AdminChatFilter(),
        lambda call: call.message.chat.type == ChatType.PRIVATE
    )
