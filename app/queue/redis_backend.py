import json
import os
import asyncio
from typing import Any, Optional
import redis.asyncio as redis

DEFAULT_REDIS_URL = "redis://localhost:6379/0"
QUEUE_KEY = os.getenv("ENROLLMENT_QUEUE_KEY", "enrollment_queue")

class RedisQueue:
    def __init__(self, url: Optional[str] = None):
        self.url = url or os.getenv("REDIS_URL", DEFAULT_REDIS_URL)
        self._client: Optional[redis.Redis] = None

    async def connect(self):
        if self._client is None:
            self._client = redis.from_url(self.url, decode_responses=True)

    async def enqueue(self, payload: dict[str, Any]):
        await self.connect()
        await self._client.lpush(QUEUE_KEY, json.dumps(payload))

    async def dequeue_batch(self, max_items: int) -> list[dict[str, Any]]:
        await self.connect()
        pipe = self._client.pipeline()
        # Use BRPOP para pegar itens (bloking pop) individualmente
        items: list[dict[str, Any]] = []
        for _ in range(max_items):
            data = await self._client.rpop(QUEUE_KEY)
            if not data:
                break
            items.append(json.loads(data))
        return items

    async def size(self) -> int:
        await self.connect()
        return await self._client.llen(QUEUE_KEY)

redis_queue = RedisQueue()
