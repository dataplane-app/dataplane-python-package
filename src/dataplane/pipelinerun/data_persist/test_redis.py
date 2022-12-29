
import os
from .redis_store import pipeline_redis_store
from .redis_store import pipeline_redis_get
import redis
from datetime import timedelta
from nanoid import generate
from dotenv import load_dotenv

def test_redis_store():

    load_dotenv()

    # ---------- Dataplane pipeline run ------------
    REDIS_HOST = os.environ["REDIS_HOST"]
    print("Redis:", REDIS_HOST)
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Data to store in Redis as parquet
    data = "hi there 123"

    # Redis connection
    redisConnect = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    
    # Store the data with key hello - run id will be attached
    rs = pipeline_redis_store(StoreKey="hello", Value=data, Redis=redisConnect, Expire=True, ExpireDuration=timedelta(minutes=15))
    print(rs)
    assert rs["result"]=="OK"

    # ---------- RETRIEVE PARQUET FROM REDIS ------------

    # Get the data
    rsget = pipeline_redis_get(StoreKey="hello", Redis=redisConnect)
    # Test before and after rows
    assert rsget["value"].decode("utf-8") == data
    assert rsget["result"]=="OK"