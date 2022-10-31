
import os
from .sharepoint_upload import sharepoint_upload
from .sharepoint_download import sharepoint_download
from nanoid import generate
import os
from dotenv import load_dotenv

def test_sharepoint_nonroot():

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

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete_non_root.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete_non_root.csv")

    # ---------- STORE File to Sharepoint ------------
    # SharepointUpload(Host, TenantID, ClientID, Secret, SiteName, TargetFilePath, SourceFilePath, FileDescription="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", FileConflict="fail")
    # print(CURRENT_DIRECTORY)
    # Store the data with key hello - run id will be attached
    rs = sharepoint_upload(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    TargetFilePath=f"/non-root myfile {RUN_ID}.csv",
    SourceFilePath=CURRENT_DIRECTORY+"/test_cities.csv",
    Library="Doc library 2",
    UploadMethod="File"
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE PARQUET FROM S3 ------------

    rs = sharepoint_download(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    SharepointFilePath=f"/non-root myfile {RUN_ID}.csv",
    LocalFilePath=CURRENT_DIRECTORY+"/test_cities_delete_non_root.csv",
    Library="Doc library 2",
    DownloadMethod="File",
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