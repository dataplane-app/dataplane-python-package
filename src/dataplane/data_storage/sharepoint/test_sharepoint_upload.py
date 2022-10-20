
import os
from .sharepoint_upload import SharepointUpload
import pandas as pd
from datetime import datetime, timedelta
from nanoid import generate
import time
import os
from dotenv import load_dotenv

def test_sharepoint_upload():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Data to store in Redis as parquet
    data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
    }
    df = pd.DataFrame(data)
    dfrows = df.shape[0]

    # Sharepoint connection
    load_dotenv()

    HOST = os.getenv('SHAREPOINT_HOST')
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')

    # ---------- STORE File to Sharepoint ------------
    
    # Store the data with key hello - run id will be attached
    rs = SharepointUpload(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane-test", 
    ProxyUse=False, ProxyUrl="", ProxyMethod="https")
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE PARQUET FROM S3 ------------

    # Get the data
    # rsget = S3Get(StoreKey="s3me", S3Client=S3Connect, Bucket=bucket)
    # print(rsget)
    # df = rsget["dataframe"]
    # print(df.shape[0])
    # # Test before and after rows
    # assert df.shape[0] == dfrows
    # assert rsget["result"]=="OK"