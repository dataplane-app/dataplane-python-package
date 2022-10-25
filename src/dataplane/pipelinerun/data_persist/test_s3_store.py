
import os
from .s3_store import pipeline_s3_store
from .s3_store import pipeline_s3_get
import boto3
from botocore.client import Config
from nanoid import generate

def test_s3_store():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Data to store as parquet
    data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
    }
    import pandas as pd
    df = pd.DataFrame(data)
    dfrows = df.shape[0]

    # S3 connection
    S3Connect = boto3.client(
        's3',
        endpoint_url="http://minio:9000",
        aws_access_key_id="admin",
        aws_secret_access_key="hello123",
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'

    )

    bucket = "dataplanebucket"

    # ---------- STORE PARQUET TO S3 ------------
    
    # Store the data with key hello - run id will be attached
    rs = pipeline_s3_store(StoreKey="s3me", DataFrame=df, S3Client=S3Connect, Bucket=bucket, Expire=False)
    print(rs)
    assert rs["result"]=="OK"

    # ---------- RETRIEVE PARQUET FROM S3 ------------

    # Get the data
    rsget = pipeline_s3_get(StoreKey="s3me", S3Client=S3Connect, Bucket=bucket)
    print(rsget)
    df = rsget["dataframe"]
    print(df.shape[0])
    # Test before and after rows
    assert df.shape[0] == dfrows
    assert rsget["result"]=="OK"