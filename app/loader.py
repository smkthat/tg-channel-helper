import asyncio
import datetime

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from app.configuration.config_loader import (
    CONFIG,
    BOT_TOKEN_FORMAT,
    check_bot_token
)
from app.configuration.log import get_logger
from app.db.database import test_connection, get_db_instance
from app.handlers.channel_handler import register_channel_handlers
from app.handlers.menu_handler import register_main_handlers
from app.handlers.user_handler import register_user_handlers
from app.middlewares.middleware import (
    DynamicDataProviderMiddleware,
    ChatThreadFilterMiddleware,
    ServicesProviderMiddleware,
    BannedMiddleware
)

LOGGER = get_logger(__name__, 'logs')


async def on_startup(bots: list[Bot]):
    await asyncio.gather(*(startup(bot) for bot in bots))


async def startup(bot: Bot):
    if bot_u := await bot.get_me():
        date = datetime.datetime.now(datetime.timezone.utc).strftime('%x %X %z')
        await bot.send_message(
            chat_id=CONFIG.bots[bot.id].owner_id,
            text=f'{bot_u.mention_markdown()} started at {date}'
        )


def register_handlers(dp):
    register_main_handlers(dp)
    register_channel_handlers(dp)
    register_user_handlers(dp)


async def start_app():
    db = get_db_instance()
    await test_connection(db)

    dp = Dispatcher(
        events_isolation=SimpleEventIsolation(),
        storage=RedisStorage(
            redis=db,
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )
    )
    dp.message.middleware.register(ServicesProviderMiddleware(db))
    dp.message.middleware.register(ChatThreadFilterMiddleware())
    dp.message.middleware.register(BannedMiddleware())
    dp.message.outer_middleware.register(DynamicDataProviderMiddleware())
    dp.startup.register(on_startup)

    register_handlers(dp)

    bots = []
    for b_data in CONFIG.bots.values():
        if check_bot_token(b_data.id) and b_data.enabled:
            bots.append(
                Bot(
                    token=dotenv.dotenv_values().get(
                        BOT_TOKEN_FORMAT.format(b_data.id)
                    ),
                    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
                )
            )

    for bot in bots:
        await bot.get_updates(offset=-1)
    await dp.start_polling(*bots)
