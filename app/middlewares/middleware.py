import os
from typing import Any, Awaitable, Callable, Dict, Union
from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatType
from aiogram.types import TelegramObject, Message, CallbackQuery
from redis.asyncio.client import Redis

from app.configuration.config_loader import CONFIG
from app.services.user_service import UserService


class DynamicDataProviderMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        data["dynamic_data"] = self.dynamic_data.get(bot.id, {})
        return await handler(event, data)

    def __init__(self):
        self.dynamic_data = CONFIG.read_yaml(
            file_path=os.path.relpath('bot_data.yaml'))


class ChatThreadFilterMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery, TelegramObject],
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.type == ChatType.SUPERGROUP:
            bot: Bot = data['bot']
            if thread_id := event.message_thread_id:
                if CONFIG.bots[bot.id].thread_id == thread_id or not \
                        CONFIG.bots[bot.id].thread_id:
                    return await handler(event, data)
        else:
            return await handler(event, data)


class DataProviderMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["bot_data"] = self.bot_data
        return await handler(event, data)

    def __init__(self, bot_data: dict):
        self.bot_data = bot_data


class ServicesProviderMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["user_service"] = UserService(self.db)
        return await handler(event, data)

    def __init__(self, db: Redis):
        self.db = db


class BannedMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery, TelegramObject],
            data: Dict[str, Any]
    ) -> Any:
        is_banned = False

        if event.chat.type == ChatType.SUPERGROUP:
            bot: Bot = data['bot']
            user_service: UserService = data['user_service']
            is_banned = await user_service.is_banned(bot.id, event.from_user.id)

        if not is_banned:
            return await handler(event, data)
