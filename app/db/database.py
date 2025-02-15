import dotenv
from redis.asyncio.client import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

from app.configuration.config_loader import CONFIG
from app.configuration.log import get_logger

LOGGER = get_logger(__name__, 'logs/redis')

INPUT_KEY_FORMAT = 'input:{bot_id}:{forwarded_message_id}'
BANNED_KEY_FORMAT = 'banned:{bot_id}'


def get_db_instance() -> Redis:
    return Redis(
        host=CONFIG.redis.host,
        port=CONFIG.redis.port,
        password=dotenv.dotenv_values().get('REDIS_PASSWORD', ''),
        db=CONFIG.redis.db,
    )


async def test_connection(db: Redis) -> None:
    try:
        await db.ping()
        LOGGER.debug('database connected [OK]')
    except RedisConnectionError as ce:
        LOGGER.fatal(ce)
        raise ce
