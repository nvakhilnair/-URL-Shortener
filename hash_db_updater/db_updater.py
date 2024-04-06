import asyncio

import pymongo
import redis.asyncio as redis

from config import settings
from logger import Logger


class DBUpdater:
    def __init__(self) -> None:
        self.logger = Logger().logger
        self.redis_settings = settings.get("redis")
        self.mongo_settings = settings.get("mongo")
        self.redis_client = redis.Redis(
            host=self.redis_settings.get("host"),
            port=self.redis_settings.get("port"),
            db=self.redis_settings.get("database"),
            decode_responses=True,
            auto_close_connection_pool=True,
        )
        self.mongo_client = pymongo.MongoClient(
            f"mongodb://{self.mongo_settings.get('host')}:{self.mongo_settings.get('port')}/"
        )
        self.mongo_db_client = self.mongo_client[self.mongo_settings.get("database")]
        self.mongo_db_col = self.mongo_db_client[
            self.mongo_settings.get("url_collection")
        ]
        self.mongo_db_col_ip = self.mongo_db_client[
            self.mongo_settings.get("ip_collection")
        ]
        self.ips = []
        self.timeout = settings.TIMEOUT

    async def push_data_from_redis_to_mongodb(self):
        self.logger.warning("Process Started")
        while True:
            if await self.redis_client.hlen("url_hashes") > 0:
                async with await self.redis_client.pipeline() as pipe:
                    await self.async_hgetall(pipe, "url_hashes")
                    await pipe.delete("url_hashes")
                    results = await self.async_execute(pipe)
                for hash_id, url in results[0].items():
                    url_hash = {
                        "hash_id": hash_id,
                        "url": url,
                    }
                    await self.async_insert_one(url_hash)
            else:
                self.logger.warning("HASH empty in redis")
            await asyncio.sleep(self.timeout)  # Adjust sleep duration as needed

    async def async_hgetall(self, pipe, key):
        return await pipe.hgetall(key)

    async def async_execute(self, pipe):
        return await pipe.execute()

    async def async_insert_one(self, document):
        self.mongo_db_col.insert_one(document)


if __name__ == "__main__":
    updater = DBUpdater()
    asyncio.run(updater.push_data_from_redis_to_mongodb())
