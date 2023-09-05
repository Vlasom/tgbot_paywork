import redis

redis_client = redis.Redis(host='localhost', db=1)

async def close_redis():
    redis_client.close()
