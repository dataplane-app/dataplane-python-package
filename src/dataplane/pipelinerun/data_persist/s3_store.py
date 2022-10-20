

import pandas as pd
# import requests
import os
from io import BytesIO
from datetime import datetime, timedelta

""" StoreKey: is the key to look up for retrieval later on. 
S3Client: e.g. S3Client = boto3.client(...)
Bucket: Name of the s3 bucket
DataFrame: Pandas dataframe to pass
Expire: Expires the data if true.
ExpireDuration: If expires is true, how much time to expire. Default 15 mins
"""
def S3Store(StoreKey, DataFrame, S3Client, Bucket, Expire=True, ExpireDuration=timedelta(days=30)):

    # Start the timer
    start  = datetime.now()

    InsertKey = "/dataplane-transfer/" + StoreKey+ "-" +os.getenv("DP_RUNID")+".parquet"

    output_buffer=BytesIO()
    DataFrame.to_parquet(output_buffer,index=False,compression='gzip',engine='pyarrow',allow_truncated_timestamps=True)
    S3Client.put_object(Bucket=Bucket,Key=InsertKey,Body=output_buffer.getvalue())
    
    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey} 


"""
StoreKey: is the key to look up for retrieval (set with RedisStore). 
S3Client: e.g. S3Client = boto3.client(...)
Bucket: Name of the s3 bucket
"""
def S3Get(StoreKey, S3Client, Bucket):

    # Start the timer
    start  = datetime.now()

    InsertKey = "/dataplane-transfer/" + StoreKey+ "-" +os.getenv("DP_RUNID")+".parquet"

    # Retrieve dataframe from key
    # buffer = BytesIO()
    objectGet = S3Client.get_object(Bucket=Bucket, Key=InsertKey, ChecksumMode='ENABLED')["Body"].read()
    df = pd.read_parquet(BytesIO(objectGet))

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "key":InsertKey,"dataframe": df}