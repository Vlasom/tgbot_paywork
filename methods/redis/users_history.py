from methods.redis.processes_redis import redis_client


async def add_history(user_tg_id: int, vacancy_id: int) -> bool:
    try:
        redis_client.sadd(f"{user_tg_id}_history", vacancy_id)
        redis_client.expire(f"{user_tg_id}_history", 86400)
        return True

    except Exception as ex:
        return False


async def get_history(user_tg_id: int) -> set | bool:
    history = redis_client.smembers(f"{user_tg_id}_history")

    if history:
        return history
    else:
        return False


