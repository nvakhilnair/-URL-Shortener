import pymongo
import redis.asyncio as redis

from url_shortener.config import settings


class DBClients:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # Initialize Redis client
            cls._instance.redis_setting = settings.get("redis")
            cls._instance.mongo_setting = settings.get("mongo")
            cls._instance.redis_client = redis.Redis(
                host=cls._instance.redis_setting.get("host"),
                port=cls._instance.redis_setting.get("port"),
                db=cls._instance.redis_setting.get("database"),
                decode_responses=True,
            )
            # Initialize MongoDB client
            cls._instance.mongo_client = pymongo.MongoClient(
                f"mongodb://{cls._instance.mongo_setting.get('host')}:{cls._instance.mongo_setting.get('port')}/"
            )
            cls._instance.mongo_db_client = cls._instance.mongo_client[
                cls._instance.mongo_setting.get("database")
            ]
            cls._instance.mongo_db_col = cls._instance.mongo_db_client[
                cls._instance.mongo_setting.get("url_collection")
            ]
        return cls._instance
