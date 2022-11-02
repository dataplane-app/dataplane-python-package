"""
S3Client: Client for s3
SourceFilePath: /tmp/source.xlsx (needs UploadMethod="File")
TargetFilePath: /General/hello.xlxs
UploadMethod: Object or File
"""

def s3_upload(S3Client, Bucket, TargetFilePath, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject=""):

    from datetime import datetime
    from io import BytesIO

    start = datetime.now()

    # Connect to S3 Bucket

    # ====== Obtain the file from disk ======
    if UploadMethod == "File":
        with open(SourceFilePath, 'rb') as data:
            S3Client.upload_fileobj(Fileobj=data, Bucket=Bucket, Key=TargetFilePath)
            duration = datetime.now() - start
            return {"result":"OK", "duration": str(duration), "Path":TargetFilePath}

    # ====== Upload file using boto3 upload_file ======
    S3Client.upload_fileobj(Fileobj=BytesIO(UploadObject), Bucket=Bucket, Key=TargetFilePath)

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration)}