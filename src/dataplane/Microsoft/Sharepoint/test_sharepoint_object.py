
import os
from .sharepoint_upload import sharepoint_upload
from .sharepoint_download import sharepoint_download
from nanoid import generate
import os
from dotenv import load_dotenv

def test_sharepoint_object():

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

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete_object.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete_object.csv")

    # ---------- STORE File to Sharepoint ------------
    # SharepointUpload(Host, TenantID, ClientID, Secret, SiteName, TargetFilePath, SourceFilePath, FileDescription="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", FileConflict="fail")
    print(CURRENT_DIRECTORY)

    FileSize = os.path.getsize(CURRENT_DIRECTORY+"/test_cities.csv")
    print("File size dir:", FileSize)
    UploadObject = open(CURRENT_DIRECTORY+"/test_cities.csv", 'rb').read()
    # Store the data with key hello - run id will be attached
    rs = sharepoint_upload(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    TargetFilePath=f"/General/object myfile {RUN_ID}.csv",
    UploadObject=UploadObject,
    UploadMethod="Object"
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE PARQUET FROM S3 ------------

    rs = sharepoint_download(Host=HOST, 
    TenantID=AZURE_TENANT_ID, 
    ClientID=AZURE_CLIENT_ID, 
    Secret=AZURE_CLIENT_SECRET, 
    SiteName="Dataplane Python", 
    SharepointFilePath=f"/General/object myfile {RUN_ID}.csv",
    DownloadMethod="Object",
    ProxyUse=False, ProxyUrl="", ProxyMethod="https")
    # print(rs)
    assert rs["result"]=="OK"

    with open(CURRENT_DIRECTORY+"/test_cities_delete_object.csv", 'wb') as f:
        f.write(rs["content"])
    # Get the data
    # rsget = S3Get(StoreKey="s3me", S3Client=S3Connect, Bucket=bucket)
    # print(rsget)
    # df = rsget["dataframe"]
    # print(df.shape[0])
    # # Test before and after rows
    # assert df.shape[0] == dfrows
    # assert rsget["result"]=="OK"