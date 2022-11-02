
import os
from .pandas_redis_store import pipeline_pandas_redis_store
from .pandas_redis_store import pipeline_pandas_redis_get
import redis
from datetime import timedelta
from nanoid import generate

def test_redis_store():

    # ---------- Dataplane pipeline run ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Data to store in Redis as parquet
    data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
    }
    import pandas as pd
    df = pd.DataFrame(data)
    dfrows = df.shape[0]

    # Redis connection
    redisConnect = redis.Redis(host='redis-service', port=6379, db=0)

    
    # ---------- STORE PARQUET TO REDIS ------------
    
    # Store the data with key hello - run id will be attached
    rs = pipeline_pandas_redis_store(StoreKey="hello", DataFrame=df, Redis=redisConnect, Expire=True, ExpireDuration=timedelta(minutes=15))
    print(rs)
    assert rs["result"]=="OK"

    # ---------- RETRIEVE PARQUET FROM REDIS ------------

    # Get the data
    rsget = pipeline_pandas_redis_get(StoreKey="hello", Redis=redisConnect)
    print(rsget)
    df = rsget["dataframe"]
    print(df.shape[0])
    # Test before and after rows
    assert df.shape[0] == dfrows
    assert rsget["result"]=="OK"