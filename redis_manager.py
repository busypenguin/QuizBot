import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


redis_host = REDIS_HOST
redis_port = REDIS_PORT
redis_password = REDIS_PASSWORD

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=0,
    password=redis_password,
    decode_responses=True,
    encoding_errors='replace'
    )
