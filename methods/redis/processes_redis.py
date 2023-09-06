import redis

redis_client = redis.Redis(host='localhost', db=1, charset="utf-8", decode_responses=True)

async def close_redis():
    redis_client.close()
