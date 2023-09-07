from processes_redis import redis_client


def add_history(user_tg_id: int, id: list) -> None:
    redis_client.sadd(f"{user_tg_id}_history", *id)
    redis_client.expire(f"{user_tg_id}_history", 86400)


def check_history(user_tg_id: int, id: list) -> list:  # 1.0432917000143789
    set_res = set(id) - set(map(int, redis_client.smembers(f"{user_tg_id}_history")))
    return list(set_res)
