from processes_redis import redis_client


def create_queue(user_tg_id: int, id: list):
    n = 0
    for status in redis_client.smismember(f"{user_tg_id}_history", *id):
        if status == 0:
            redis_client.lpush(f"{user_tg_id}", id[n])
        n += 1

    redis_client.expire(f"{user_tg_id}", 86400)


def get_vacancies_id(user_tg_id: int, amount=1) -> list:
    ids = redis_client.rpop(f"{user_tg_id}", amount)
    redis_client.sadd(f"{user_tg_id}_history", *ids)
    redis_client.expire(f"{user_tg_id}", 86400)
    redis_client.expire(f"{user_tg_id}_history", 86400)

    return ids




# print(redis_client.smismember("12", "1", "2", "7"))
create_queue(1234, [7, 12])
#print(get_vacancies_id(1234, 2))





