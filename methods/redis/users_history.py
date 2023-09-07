from processes_redis import redis_client


async def add_history(user_tg_id: int, id: list) -> None:
    redis_client.sadd(f"{user_tg_id}_history", *id)
    redis_client.expire(f"{user_tg_id}_history", 86400)



def get_history(user_tg_id: int) -> set | None:
    history = redis_client.smembers(f"{user_tg_id}_history")
    if history:
        return history

