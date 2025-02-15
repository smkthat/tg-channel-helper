from typing import Union

from redis.asyncio import Redis

BANNED_KEY = 'banned:{bot_id}'
FORWARD_MESSAGE_KEY = 'input:{bot_id}:{forwarded_message_id}'


class UserService:

    def __init__(self, db: Redis):
        self.db = db

    async def get_user(self, bot_id: int, forward_message_id: int) -> Union[None, int]:
        query = FORWARD_MESSAGE_KEY.format(bot_id=bot_id, forwarded_message_id=forward_message_id)
        user_id = await self.db.get(query)
        return int(user_id) if user_id else None

    async def get_banned_users(self, bot_id: int) -> list[int]:
        query = BANNED_KEY.format(bot_id=bot_id)
        return list(map(int, await self.db.lrange(query, 0, -1)))

    async def ban_user(self, bot_id: int, user_id: int) -> int:
        query = BANNED_KEY.format(bot_id=bot_id)
        return await self.db.lpush(query, user_id)

    async def unban_user(self, bot_id: int, user_id: int) -> int:
        query = BANNED_KEY.format(bot_id=bot_id)
        return await self.db.lrem(query, 1, str(user_id))

    async def is_banned(self, bot_id: int, user_id: int) -> bool:
        banned_users = await self.get_banned_users(bot_id)
        return int(user_id) in banned_users

    async def set_user_link(self, bot_id: int, message_id: int, user_id: int) -> None:
        query = FORWARD_MESSAGE_KEY.format(bot_id=bot_id, forwarded_message_id=message_id)
        await self.db.append(query, user_id)

