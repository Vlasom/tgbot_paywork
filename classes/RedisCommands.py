from .Users import User
from .Vacancies import Vacancy
import redis


class RedisCommands:
    def __init__(self):
        self.redis_client: redis.Redis = redis.Redis(host='localhost', db=1, charset="utf-8", decode_responses=True)

    async def close_conn(self):
        self.redis_client.close()

    async def user_add_history(self, user: User, vacancy: Vacancy):
        try:
            await self.redis_client.sadd(f"{user.tg_id}_history", vacancy.id)
            await self.redis_client.expire(f"{user.tg_id}_history", 86400)
            return True

        except Exception as ex:
            return False

    async def user_get_history(self, user: User) -> set | bool:
        history = self.redis_client.smembers(f"{user.tg_id}_history")

        if history:
            return history
        else:
            return False