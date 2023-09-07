from processes_redis import redis_client
import timeit


def add_history(user_tg_id: int, id: list) -> None:
    redis_client.sadd(f"{user_tg_id}_history", *id)
    redis_client.expire(f"{user_tg_id}_history", 86400)


def check_history(user_tg_id: int, id: list): #2.1188024999573827
    check_res = redis_client.smismember(f"{user_tg_id}_history", *id)
    unique_id = [id[i] for i in range(len(id)) if check_res[i] == 0]
    redis_client.expire(f"{user_tg_id}_history", 86400)

    print(unique_id)


def check_history2(user_tg_id: int, id: list): #3.7813390000374056
    redis_client.sadd(f"{user_tg_id}_check", *id)
    unique_id = redis_client.sdiff(f"{user_tg_id}_check", f"{user_tg_id}_history")
    redis_client.delete(f"{user_tg_id}_check")
    redis_client.expire(f"{user_tg_id}_history", 86400)

    print(unique_id)


# add_history(12345, [2, 5, 7])
print(timeit.timeit("check_history2(12345, [1, 2, 3, 4])", globals={"check_history2": check_history2, },
                    number=1000))
