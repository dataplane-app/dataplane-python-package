
import os
from .s3_download import s3_download
from .s3_upload import s3_upload
from nanoid import generate
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

def test_s3_object():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Sharepoint connection
    load_dotenv()

    RUN_ID = os.environ["DP_RUNID"]

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

    CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete_object.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete_object.csv")

    # ---------- STORE File to S3 ------------
    # s3_upload(Bucket, AccessKey, SecretKey, TargetFilePath, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", EndPointUrl=None)
    print(CURRENT_DIRECTORY)

    FileSize = os.path.getsize(CURRENT_DIRECTORY+"/test_s3_cities.csv")
    print("File size dir:", FileSize)
    UploadObject = open(CURRENT_DIRECTORY+"/test_s3_cities.csv", 'rb').read()
    # Store the data with key hello - run id will be attached
    rs = s3_upload(Bucket=bucket, 
    S3Client=S3Connect,
    TargetFilePath=f"/s3test/object myfile {RUN_ID}.csv",
    UploadObject=UploadObject,
    UploadMethod="Object"
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE FILE FROM S3 ------------
    rs = s3_download(Bucket=bucket, 
    S3Client=S3Connect,
    S3FilePath=f"/s3test/object myfile {RUN_ID}.csv",
    DownloadMethod="Object"
    )
    print(rs)
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