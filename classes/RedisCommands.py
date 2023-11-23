from .Users import User
from .Vacancies import Vacancy
import redis
from .sql_conn import sql_connection as sql_conn


class RedisCommands:
    def __init__(self):
        self.redis_client: redis.Redis = redis.Redis(host='localhost', db=1, charset="utf-8", decode_responses=True)

    async def close_conn(self) -> None:
        self.redis_client.close()

    async def verify(self, user_tg_id):
        sql_conn.cur.execute("UPDATE users SET verification = 1 WHERE tg_id = ?", (user_tg_id,))
        sql_conn.conn.commit()
        return self.redis_client.sadd("verified_users", user_tg_id)

    async def load_verified_users(self):
        sql_conn.cur.execute("SELECT tg_id FROM users WHERE verification = 1")
        return self.redis_client.sadd("verified_users", *[i[0] for i in sql_conn.cur.fetchall()])

    async def user_add_history(self, user: User, vacancy: Vacancy) -> bool:
        try:
            await self.redis_client.sadd(f"{user.tg_id}_history", vacancy.id)
            return True

        except Exception as ex:
            return False

    async def user_get_history(self, user: User) -> set | bool:
        history = self.redis_client.smembers(f"{user.tg_id}_history")

        if history:
            return history
        else:
            return False

    async def user_del_history(self, user: User) -> None | bool:
        try:
            await self.redis_client.delete(f"{user.tg_id}_history")

        except Exception as ex:
            return False

    async def add_last_action_status(self, user: User) -> None:
        return self.redis_client.set(f"{user.tg_id}_last_action_status", 1, ex=2)

    async def del_last_action_status(self, user: User) -> None:
        return self.redis_client.delete(f"{user.tg_id}_last_action_status")

    async def check_last_action_status(self, user: User) -> bool:
        per = self.redis_client.get(f"{user.tg_id}_last_action_status")
        return bool(per)

    async def check_verification(self, user: User):
        return self.redis_client.sismember("verified_users", str(user.tg_id))
