from datetime import timedelta

def RedisCheck(r):

    import redis

    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print("Redis connection error.", redis.exceptions.ConnectionError, ConnectionRefusedError)
        return False
    return True

""" StoreKey: is the key to look up for retrieval later on. 
Redis: e.g. Redis = redis.Redis(host='redis-service', port=6379, db=0)
DataFrame: Pandas dataframe to pass
Expire: Expires the data if true.
ExpireDuration: If expires is true, how much time to expire. Default 15 mins
"""
def pipeline_pandas_redis_store(StoreKey, DataFrame, Redis, Expire=True, ExpireDuration=timedelta(minutes=15)):

    import os
    import io
    from datetime import datetime

    # Start the timer
    start  = datetime.now()

    InsertKey = StoreKey+ "-" +os.getenv("DP_RUNID")

    # Connect to Redis
    if RedisCheck(Redis) == False:
        raise Exception("Redis connection failed.")

    buffer = io.BytesIO()
    DataFrame.to_parquet(buffer, compression='gzip')
    buffer.seek(0) # re-set the pointer to the beginning after reading

    if Expire:
        Redis.setex(InsertKey, ExpireDuration, value=buffer.read())
    else:
        Redis.set(InsertKey, value=buffer.read())
    
    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey} 


"""
StoreKey: is the key to look up for retrieval (set with RedisStore). 
Redis: e.g. Redis = redis.Redis(host='redis-service', port=6379, db=0)
"""
def pipeline_pandas_redis_get(StoreKey, Redis):

    import os
    import io
    from datetime import datetime

    # Start the timer
    start  = datetime.now()

    InsertKey = StoreKey+ "-" +os.getenv("DP_RUNID")

    # Connect to Redis
    if RedisCheck(Redis) == False:
        raise Exception("Redis connection failed.")

    # Retrieve dataframe from key
    buffer = io.BytesIO(Redis.get(InsertKey))
    buffer.seek(0)
    import pandas as pd
    df = pd.read_parquet(buffer)

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey,"dataframe": df}