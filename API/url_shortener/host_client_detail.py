from url_shortener.db_clients import DBClients


async def push_client_ip_to_redis(client_ip):
    clients = DBClients()
    redis_client = clients.redis_client
    await redis_client.sadd("IPs", client_ip)
