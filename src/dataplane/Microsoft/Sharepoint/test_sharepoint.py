
import os
from .sharepoint_upload import SharepointUpload
from .sharepoint_download import SharepointDownload
from datetime import datetime, timedelta
from nanoid import generate
import time
import os
from dotenv import load_dotenv

def test_sharepoint():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Sharepoint connection
    load_dotenv()

    RUN_ID = os.environ["DP_RUNID"]
    HOST = os.getenv('SHAREPOINT_HOST')
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
    CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

    # ---------- STORE File to Sharepoint ------------
    # SharepointUpload(Host, TenantID, ClientID, Secret, SiteName, TargetFilePath, SourceFilePath, FileDescription="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", FileConflict="fail")
    print(CURRENT_DIRECTORY)
    # Store the data with key hello - run id will be attached
    rs = SharepointUpload(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    TargetFilePath=f"/General/myfile {RUN_ID}.csv",
    SourceFilePath=CURRENT_DIRECTORY+"/test_cities.csv"
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE PARQUET FROM S3 ------------

    rs = SharepointDownload(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    SharepointFilePath=f"/General/myfile {RUN_ID}.csv",
    LocalFilePath=CURRENT_DIRECTORY+"/test_cities_delete.csv",
    ProxyUse=False, ProxyUrl="", ProxyMethod="https")
    print(rs)
    assert rs["result"]=="OK"
    # Get the data
    # rsget = S3Get(StoreKey="s3me", S3Client=S3Connect, Bucket=bucket)
    # print(rsget)
    # df = rsget["dataframe"]
    # print(df.shape[0])
    # # Test before and after rows
    # assert df.shape[0] == dfrows
    # assert rsget["result"]=="OK"