from url_shortener.db_clients import DBClients
from url_shortener.hasher.cityhash_encoder import generate_cityhash32


class Hash:
    def __init__(self) -> None:
        clients = DBClients()
        self.redis_client = clients.redis_client
        self.mongo_db_col = clients.mongo_db_col
        self.hash_value = None

    async def get_hash(self, query):
        self.hash_value = await generate_cityhash32(query.encode())
        await self.push_url_hash_to_redis(query=query)
        return self.hash_value

    async def get_full_url(self, query):
        if await self.redis_client.hexists("url_hashes", query):
            self.url = await self.redis_client.hget("url_hashes", query)
            return self.url
        self.url = self.mongo_db_col.find_one({"hash_id": query})
        print(self.url)
        if self.url:
            self.url = self.url.get("url")
            return self.url

    async def push_url_hash_to_redis(self, query):
        if await self.redis_client.hexists("url_hashes", self.hash_value):
            return
        await self.redis_client.hset("url_hashes", self.hash_value, query)
