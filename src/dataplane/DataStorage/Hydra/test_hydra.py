import sqlalchemy
from .hydra_download import hydra_download
from .hydra_upload import hydra_upload
import os
from dotenv import load_dotenv
from nanoid import generate

def test_hydra():
    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Sharepoint connection
    load_dotenv()

    RUN_ID = os.environ["DP_RUNID"]

    DBClient = sqlalchemy.create_engine("postgresql://admin:hello123@hydra:5432/dataplanedb?sslmode=disable")

    table = 'newtable'

    CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

    if os.path.exists(CURRENT_DIRECTORY+"/test_cities_delete_object.csv"):
        os.remove(CURRENT_DIRECTORY+"/test_cities_delete_object.csv")

    # ------------- Store file to Hydra DB -------------
    print(CURRENT_DIRECTORY)
    rs = hydra_upload(
        DBClient=DBClient,
        TargetTableName=table,
        SourceFilePath=CURRENT_DIRECTORY+"/test_hydra_cities.csv",
        UploadMethod='File'
    )
    print(rs)
    assert rs['result']=='OK'


    # ------------ Retreive Table from Hydra -------------

    rs = hydra_download(
        DBClient=DBClient,
        SourceTableName=table,
        DownloadMethod="File",
        LocalFilePath=CURRENT_DIRECTORY+"/test_cities_delete.csv",
    )
    print(rs)
    assert rs["result"]=="OK"