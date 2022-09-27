import os, io, redis
from datetime import datetime, timedelta
import pandas as pd


def RedisCheck(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print("Redis connection error.", redis.exceptions.ConnectionError, ConnectionRefusedError)
        return False
    return True

"""
StoreKey: is the key to look up for retrieval later on. 
RedisHost: host of Redis e.g localhost 
RedisPort: default 6379
RedisDB: default 0
DataFrame: Pandas dataframe to pass
Expire: Expires the data if true.
ExpireDuration: If expires is true, how much time to expire. Default 15 mins
"""
def RedisStore(StoreKey, DataFrame, RedisHost="localhost", RedisPort=6379, RedisDB=0, Expire=True, ExpireDuration=timedelta(minutes=15)):

    # Start the timer
    start  = datetime.now()

    InsertKey = StoreKey+ "-" +os.getenv("DP_RUNID")

    # Connect to Redis
    r = redis.Redis(host='redis-service', port=6379, db=0)
    if RedisCheck(r) == False:
        raise Exception("Redis connection failed.")

    buffer = io.BytesIO()
    DataFrame.to_parquet(buffer, compression='gzip')
    buffer.seek(0) # re-set the pointer to the beginning after reading

    if Expire:
        r.setex(StoreKey, ExpireDuration, value=buffer.read())
    else:
        r.set(StoreKey, value=buffer.read())
    
    duration = datetime.now() - start

    return {"key":InsertKey, "result":"OK", "duration": str(duration)} 