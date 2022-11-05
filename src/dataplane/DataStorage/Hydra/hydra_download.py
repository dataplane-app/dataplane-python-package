"""
DBClient: Database Client (sqlalchemy.engine.Engine or sqlalchemy.engine.Connection)
LocalFilePath: File to write (needs DownloadMethod="File")
SourceTableName: table name in Hydra
DownloadMethod: Object or File
"""

def hydra_download(DBClient, SourceTableName, DownloadMethod="Object", LocalFilePath=""):
    
    import pandas as pd
    from datetime import datetime
    # Start the timer
    start = datetime.now()

    df = pd.read_sql_table(SourceTableName,DBClient)

    if DownloadMethod=="File":
        if LocalFilePath == "":
            duration = datetime.now() - start
            return {"result":"Fail", "duration": str(duration), "reason":"File method requires a local file file path"} 

        with open(LocalFilePath,'w') as f:
            f.write(df.to_csv())
        
        duration = datetime.now() - start
        return {"result":"OK", "duration": str(duration), "FilePath": LocalFilePath} 

    objectGet = df.to_csv().encode('utf-8')
    duration = datetime.now() - start
    return {"result":"OK", "duration": str(duration), "content": objectGet}

