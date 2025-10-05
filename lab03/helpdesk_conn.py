import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

def get_redis():
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    username = os.getenv("REDIS_USERNAME", None)
    password = os.getenv("REDIS_PASSWORD", None)
    use_ssl = os.getenv("REDIS_SSL", "false").lower() in ("1","true","yes","on")

    if use_ssl:
        r = Redis(
            host=host, port=port,
            username=username, password=password,
            ssl=True, ssl_cert_reqs=None, ssl_check_hostname=False,
            decode_responses=True, socket_timeout=10,
        )
    else:
        r = Redis(
            host=host, port=port,
            username=username, password=password,
            decode_responses=True, socket_timeout=10,
        )
    return r

if __name__ == "__main__":
    r = get_redis()
    print("PING ->", r.ping())
