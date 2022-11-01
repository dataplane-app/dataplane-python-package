""" Host: {name}.sharepoint.com 
TenantID: Directory or TenantID as per Azure portal
ClientID: Azure Client ID or Application ID.
Secret: Azure secret for client ID.
SiteName: Name of the site to be looked up <- in url e.g https://{name}.sharepoint.com/sites/DataplanePython
FilePath: /General/hello.xlxs
ProxyUse: Whether to use a proxy, true or false
ProxyUrl: Proxy endpoint to use
ProxyMethod: https or http, default https
"""

def s3_download(Bucket, AccessKey, SecretKey, S3FilePath, DownloadMethod="Object", LocalFilePath="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", EndPointUrl=None):
    
    import boto3
    from botocore.exceptions import ClientError
    from datetime import datetime
    from io import BytesIO

    # Start the timer
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
    
    # Download S3 file content
    r=BytesIO()
    print(S3FilePath[1:])
    bucket_conn.download_fileobj(S3FilePath[1:], r)

    if DownloadMethod == "File":
        with open(LocalFilePath, 'wb') as f:
            r.seek(0)
            f.write(r.read())
        duration = datetime.now() - start
        return {"result":"OK", "duration": str(duration), "status": None, "FilePath": LocalFilePath} 
    
    duration = datetime.now() - start
    return {"result":"OK", "duration": str(duration), "status": None, "content": r} 
