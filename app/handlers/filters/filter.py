from typing import Union

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import (
    Message,
    CallbackQuery,
    ChatMemberOwner,
    ChatMemberAdministrator
)

from app.configuration.config_loader import CONFIG


class AdminChatFilter(Filter):
    async def __call__(
            self,
            source: Union[Message, CallbackQuery],
            bot: Bot
    ) -> bool:
        if not source.from_user.is_bot:
            chat_member = await bot.get_chat_member(
                chat_id=CONFIG.bots[bot.id].admin_chat_id,
                user_id=source.from_user.id
            )
            return isinstance(
                chat_member, Union[ChatMemberOwner, ChatMemberAdministrator]
            )
