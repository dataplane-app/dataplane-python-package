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
Value: The value to pass
Expire: Expires the data if true.
ExpireDuration: If expires is true, how much time to expire. Default 15 mins
"""
def pipeline_redis_store(StoreKey, Value, Redis, Expire=True, ExpireDuration=timedelta(minutes=15)):

    import os
    import io
    from datetime import datetime

    # Start the timer
    start  = datetime.now()

    InsertKey = StoreKey+ "-" +os.getenv("DP_RUNID")

    # Connect to Redis
    if RedisCheck(Redis) == False:
        raise Exception("Redis connection failed.")

    if Expire:
        Redis.setex(InsertKey, ExpireDuration, value=Value)
    else:
        Redis.set(InsertKey, value=Value)
    
    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey} 


"""
StoreKey: is the key to look up for retrieval (set with RedisStore). 
Redis: e.g. Redis = redis.Redis(host='redis-service', port=6379, db=0)
"""
def pipeline_redis_get(StoreKey, Redis):

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
    value = Redis.get(InsertKey)

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey,"value": value}