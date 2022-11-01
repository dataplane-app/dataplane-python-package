"""
AccessKey: S3 Access Key.
SecretKey: S3 Secret Key.
SourceFilePath: /tmp/source.xlsx (needs UploadMethod="File")
TargetFilePath: /General/hello.xlxs
UploadMethod
ProxyUse: Whether to use a proxy, true or false
ProxyUrl: Proxy endpoint to use
ProxyMethod: https or http, default https
EndPointUrl: Custom endpoint URL (eg. for minio)
"""

def s3_upload(Bucket, AccessKey, SecretKey, TargetFilePath, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", EndPointUrl=None):


    import boto3
    from botocore.config import Config
    from botocore.exceptions import ClientError
    from datetime import datetime
    from io import BytesIO
    import os

    start = datetime.now()

    # Connect to S3 Bucket

    if ProxyUse:
        proxies = {ProxyMethod: ProxyUrl}
    else:
        proxies = {}

    s3_conn = boto3.resource(
        "s3",
        endpoint_url = EndPointUrl,
        aws_access_key_id=AccessKey,
        aws_secret_access_key=SecretKey,
        aws_session_token=None,
        config=boto3.session.Config(
            signature_version='s3v4',
            proxies=proxies
        ),
    )

    bucket_conn = s3_conn.Bucket(Bucket)

    try:
        _ = bucket_conn.creation_date
    except ClientError as e:
        duration = datetime.now() - start
        return {
            "result":"Fail",
            "reason":"Auth fail",
            "duration": str(duration),
            "status": None,
            "error": e
        }

    # ====== Obtain the file from disk ======
    if UploadMethod == "File":
        UploadObject = open(SourceFilePath, 'rb')
    else:
        temp_file = BytesIO()
        temp_file.write(UploadObject)
        temp_file.seek(0)
        UploadObject = temp_file

    # ====== Upload file using boto3 upload_file ======
    bucket_conn.upload_fileobj(UploadObject, TargetFilePath)

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration)}