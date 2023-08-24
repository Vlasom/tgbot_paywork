import aioredis

async def create_queue(tg_id, *id_vacs):
    await
