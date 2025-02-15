from typing import List

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message, ReactionTypeEmoji
from aiogram_media_group import media_group_handler

from app.configuration.config_loader import CONFIG
from app.configuration.log import get_logger
from app.handlers.filters.filter import AdminChatFilter
from app.handlers.states.state import ChannelSG
from app.services.user_service import UserService

LOGGER = get_logger(__name__, '../../logs')


async def user_ask(
        m: Message,
        bot: Bot,
        dynamic_data: dict,
        user_service: UserService
) -> None:
    try:
        forwarded = await m.forward(
            chat_id=CONFIG.bots[bot.id].admin_chat_id,
            message_thread_id=CONFIG.bots[bot.id].thread_id
        )
        await user_service.set_user_link(
            bot.id,
            forwarded.message_id,
            m.from_user.id
        )
        if dynamic_data['answer_message']:
            await m.reply(
                text=dynamic_data['answer_message']['text']
            )
    except TelegramBadRequest:
        msg = ('admin chat not found! please add bot to admin chat '
               f'id={CONFIG.bots[bot.id].admin_chat_id}')
        LOGGER.error(msg)


@media_group_handler
async def answer_to_user_album(
        messages: List[Message],
        bot: Bot,
        user_service: UserService
) -> None:
    first_message = messages[0]
    reply_message = first_message.reply_to_message
    if reply_message.forward_date:
        if user_id := await user_service.get_user(
                bot.id,
                reply_message.message_id
        ):
            for m in messages:
                if _ := await m.copy_to(chat_id=user_id):
                    await m.react([ReactionTypeEmoji(type='emoji', emoji='✅')])
        else:
            await first_message.answer(
                '⚠️ Пользователь не найден, сообщение не доставлено')


async def answer_to_user(
        m: Message,
        bot: Bot,
        user_service: UserService
) -> None:
    text = m.text or m.caption

    if text.startswith('/') and not text.startswith('/start'):
        await m.answer('❌ Не правильная команда')
        return

    reply_message = m.reply_to_message
    if reply_message.forward_date:
        if user_id := await user_service.get_user(
                bot.id,
                reply_message.message_id
        ):
            if _ := await m.copy_to(chat_id=user_id):
                await m.react([ReactionTypeEmoji(type='emoji', emoji='✅')])
        else:
            await m.answer('⚠️ Пользователь не найден, сообщение не доставлено')


def register_user_handlers(dp: Dispatcher):
    dp.message.register(
        answer_to_user_album,
        F.media_group_id,
        AdminChatFilter(),
        lambda message: message.chat.type == ChatType.SUPERGROUP,
        lambda message: message.reply_to_message,
        lambda message: message.reply_to_message.forward_date,
        ~StateFilter(ChannelSG),
    )
    dp.message.register(
        answer_to_user,
        AdminChatFilter(),
        lambda message: message.chat.type == ChatType.SUPERGROUP,
        lambda message: message.reply_to_message,
        lambda message: message.reply_to_message.forward_date,
        ~StateFilter(ChannelSG),
    )
    dp.message.register(
        user_ask,
        lambda message: message.chat.type == ChatType.PRIVATE,
        ~StateFilter(ChannelSG)
    )
