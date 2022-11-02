""" 
S3Client: Client for s3
S3FilePath: /tmp/source.xlsx (needs UploadMethod="File")
LocalFilePath: /General/hello.xlxs (where download method is File)
Download Method: File or Object
FilePath: /General/hello.xlxs
"""

def s3_download(S3Client, Bucket,  S3FilePath, DownloadMethod="Object", LocalFilePath=""):
    
    from datetime import datetime
    from io import BytesIO

    # Start the timer
    start = datetime.now()
    
    # Download S3 file content to file - uses multi threaded download
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj

    if DownloadMethod == "File":
        if LocalFilePath == "":
            duration = datetime.now() - start
            return {"result":"Fail", "duration": str(duration), "reason":"File method requires a local file file path"} 

        with open(LocalFilePath, 'wb') as data:
            S3Client.download_fileobj(Bucket=Bucket, Key=S3FilePath, Fileobj=data)

        duration = datetime.now() - start
        return {"result":"OK", "duration": str(duration), "FilePath": LocalFilePath} 

    # Download S3 file content to object
    objectGet = S3Client.get_object(Bucket=Bucket, Key=S3FilePath, ChecksumMode='ENABLED')["Body"].read()
    
    duration = datetime.now() - start
    return {"result":"OK", "duration": str(duration), "content": objectGet} 
