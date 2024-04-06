import asyncio

import aiohttp
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
        mongo_client = pymongo.MongoClient(
            f"mongodb://{self.mongo_settings.get('host')}:{self.mongo_settings.get('port')}/"
        )
        mongo_db_client = mongo_client[self.mongo_settings.get("database")]
        self.mongo_db_col = mongo_db_client[self.mongo_settings.get("url_collection")]
        self.mongo_db_col_ip = mongo_db_client[self.mongo_settings.get("ip_collection")]
        self.timeout = settings.TIMEOUT
        self.request_headers = {
            "authority": "api.ipgeolocation.io",
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://ipgeolocation.io",
            "pragma": "no-cache",
            "referer": "https://ipgeolocation.io/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

    async def append_ips_from_redis_to_list(self):
        while True:
            ips = await self.get_ips_from_redis()
            if ips:
                self.logger.info("IPs Set Found in redis")
                await self.process_ips(ips)
            else:
                self.logger.warning("IPs Set empty in redis")
            await asyncio.sleep(self.timeout)

    async def get_ips_from_redis(self):
        return await self.redis_client.smembers("IPs")

    async def fetch_ip_data(self, ip):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"https://api.ipgeolocation.io/ipgeo?include=hostname&ip={ip}",
                    headers=self.request_headers,
                ) as response:
                    return await response.json()
            except Exception:
                return {}

    async def process_ips(self, ips):
        tasks = [self.fetch_ip_data(ip) for ip in ips]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            ip_details = {
                "ip": response.get("ip", "127.0.0.1"),
                "country": response.get("country_name", "Local network"),
                "region": response.get("continent_name", "Local network"),
            }
            self.mongo_db_col_ip.insert_one(ip_details)
        await self.clear_ips_from_redis(ips)

    async def clear_ips_from_redis(self, ips):
        async with await self.redis_client.pipeline() as pipe:
            for ip in ips:
                await pipe.srem("IPs", ip)
            await pipe.execute()


if __name__ == "__main__":
    updater = DBUpdater()
    asyncio.run(updater.append_ips_from_redis_to_list())
