
import os
from dataplane.DataStorage.s3.s3_download import s3_download
from dataplane.DataStorage.s3.s3_upload import s3_upload
from nanoid import generate
import os
from dotenv import load_dotenv

def test_s3_object():

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

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete_object.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete_object.csv")

    # ---------- STORE File to S3 ------------
    # s3_upload(Bucket, AccessKey, SecretKey, TargetFilePath, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", EndPointUrl=None)
    print(CURRENT_DIRECTORY)

    FileSize = os.path.getsize(CURRENT_DIRECTORY+"/test_cities.csv")
    print("File size dir:", FileSize)
    UploadObject = open(CURRENT_DIRECTORY+"/test_cities.csv", 'rb').read()
    # Store the data with key hello - run id will be attached
    rs = s3_upload(Bucket=BUCKET, 
    AccessKey=ACCESS_KEY, 
    SecretKey=SECRET_KEY,
    TargetFilePath=f"/General/object myfile {RUN_ID}.csv",
    UploadObject=UploadObject,
    UploadMethod="Object",
    EndPointUrl='http://minio:9000'
    )
    print(rs)
    assert rs["result"]=="OK"


    # ---------- RETRIEVE FILE FROM S3 ------------
    rs = s3_download(Bucket=BUCKET, 
    AccessKey=ACCESS_KEY, 
    SecretKey=SECRET_KEY,
    S3FilePath=f"/General/object myfile {RUN_ID}.csv",
    DownloadMethod="Object",
    ProxyUse=False, ProxyUrl="", ProxyMethod="https",
    EndPointUrl='http://minio:9000'
    )
    print(rs)
    assert rs["result"]=="OK"

    # with open(CURRENT_DIRECTORY+"/test_cities_delete_object.csv", 'wb') as f:
    #     f.write(rs["content"])
    # Get the data
    # rsget = S3Get(StoreKey="s3me", S3Client=S3Connect, Bucket=bucket)
    # print(rsget)
    # df = rsget["dataframe"]
    # print(df.shape[0])
    # # Test before and after rows
    # assert df.shape[0] == dfrows
    # assert rsget["result"]=="OK"