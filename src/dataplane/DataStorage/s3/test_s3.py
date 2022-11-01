
import os
from dataplane.DataStorage.s3.s3_upload import s3_upload
from dataplane.DataStorage.s3.s3_download import s3_download
from nanoid import generate
import os
from dotenv import load_dotenv

def test_s3():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Sharepoint connection
    load_dotenv()

    RUN_ID = os.environ["DP_RUNID"]
    BUCKET = os.getenv('BUCKET')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete.csv")

    # ---------- STORE File to Sharepoint ------------
    # s3_upload(Bucket, AccessKey, SecretKey, TargetFilePath, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", EndPointUrl=None)
    print(CURRENT_DIRECTORY)
    # Store the data with key hello - run id will be attached
    rs = s3_upload(Bucket=BUCKET,
    AccessKey=ACCESS_KEY, 
    SecretKey=SECRET_KEY,
    TargetFilePath=f"/General/myfile {RUN_ID}.csv",
    SourceFilePath=CURRENT_DIRECTORY+"/test_cities.csv",
    UploadMethod="File",
    EndPointUrl="http://minio:9000"
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE PARQUET FROM S3 ------------

    rs = s3_download(Bucket=BUCKET, 
    AccessKey=ACCESS_KEY, 
    SecretKey=SECRET_KEY,
    S3FilePath=f"/General/myfile {RUN_ID}.csv",
    LocalFilePath=CURRENT_DIRECTORY+"/test_cities_delete.csv",
    DownloadMethod="File",
    ProxyUse=False, ProxyUrl="", ProxyMethod="https",
    EndPointUrl='http://minio:9000'
    )
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