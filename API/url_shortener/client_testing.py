
import redis

from url_shortener.db_clients import DBClients
from url_shortener.logger import Logger


class DBClientPing:
    def __init__(self) -> None:
        self.clients = DBClients()
        self.logger = Logger().logger
        self.test_redis_connection()
        self.test_mongo_connection()

    def test_redis_connection(self):
        try:
            redis_client = self.clients.redis_client
            response = redis_client.ping()
            if response:
                self.logger.info("Redis connection successful.")
            else:
                self.logger.error("Failed to ping Redis server.")
                raise ConnectionError("Failed to ping Redis server.")
        except redis.ConnectionError:
            self.logger.error("Failed to connect to Redis server.")
            raise ConnectionError("Failed to connect to Redis server.")

    def test_mongo_connection(self):
        try:
            mongo_client = self.clients.mongo_client
            response = mongo_client.server_info()
            if response:
                self.logger.info("MongoDB connection successful.")
            else:
                self.logger.error("Failed to ping MongoDB server.")
                raise ConnectionError("Failed to ping MongoDB server.")
        except Exception:
            self.logger.error("Failed to connect to MongoDB server.")
            raise ConnectionError("Failed to connect to MongoDB server.")
