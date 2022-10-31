""" Host: {name}.sharepoint.com 
TenantID: Directory or TenantID as per Azure portal
ClientID: Azure Client ID or Application ID.
Secret: Azure secret for client ID.
SiteName: Name of the site to be looked up <- in url e.g https://{name}.sharepoint.com/sites/DataplanePython
SourceFilePath: /tmp/source.xlsx (needs UploadMethod="File")
TargetFilePath: /General/hello.xlxs
UploadMethod
ProxyUse: Whether to use a proxy, true or false
ProxyUrl: Proxy endpoint to use
ProxyMethod: https or http, default https
FileConflict: "fail (default) | replace | rename"
FileDescription: Sharepoint description for the file
"""
def sharepoint_upload(Host, TenantID, ClientID, Secret, SiteName, TargetFilePath, SourceFilePath="/tmp/default.txt", Library="root", UploadMethod="Object", UploadObject="", ProxyUse=False, ProxyUrl="", ProxyMethod="https", FileConflict="fail"):


    import requests
    import os
    from datetime import datetime
    import json
    import sys

    # Start the timer
    start  = datetime.now()

    # ===== Authenticate with Sharepoint ======

    url = f"https://login.microsoftonline.com/{TenantID}/oauth2/v2.0/token"

    payload=f""" 
    client_id={ClientID}
    &scope=https://graph.microsoft.com/.default
    &client_secret= {Secret}
    &grant_type=client_credentials
    """

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    if ProxyUse==True:
        proxies = {ProxyMethod: ProxyUrl}
    else:
        proxies = {}

    auth = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    
    if auth.status_code != 200:
        duration = datetime.now() - start
        return {"result":"Fail", "reason":"Auth fail", "duration": str(duration), "status": auth.status_code, "error": auth.json()} 


    auth = auth.json()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    # ======= Get Site ID from Site name ====
    SiteName = SiteName.replace(" ", "")
    SiteID = requests.request("GET", f"https://graph.microsoft.com/v1.0/sites/{Host}:/sites/{SiteName}", headers=headers, json=payload, proxies=proxies)
    
    if SiteID.status_code != 200:
        duration = datetime.now() - start
        return {"result":"Fail", "reason":"Get site ID", "duration": str(duration), "status": SiteID.status_code, "error": SiteID.json()} 

    SiteID = SiteID.json()

    # print(SiteID)

    # ====== Library
    # Note the target path must have a / prefix
    TargetFilePath = TargetFilePath.replace(" ", "%20")
    drive = "root"
    if Library == "root":
        # ====== Create an upload session =====
        url = f"https://graph.microsoft.com/v1.0/sites/{SiteID['id']}/drive/root:{TargetFilePath}:/createUploadSession"
    else:

        drive = ""
        driveID = requests.request("GET", f"https://graph.microsoft.com/v1.0/sites/{SiteID['id']}/drives?$select=name,id", headers=headers, json=payload, proxies=proxies)
        if driveID.status_code != 200:
            duration = datetime.now() - start
            return {"result":"Fail", "reason":"Sharepoint get drives", "duration": str(duration), "status": driveID.status_code, "error": driveID.json()} 
        
        driveID = driveID.json()
        for x in driveID["value"]:
            if x["name"] == Library:
                drive = x["id"]
                break
        
        if drive =="":
            duration = datetime.now() - start
            return {"result":"Fail", "reason":"Sharepoint no drove found fpr library "+Library, "duration": str(duration)} 
        
        url = f"https://graph.microsoft.com/v1.0/sites/{SiteID['id']}/drives/{drive}/root:{TargetFilePath}:/createUploadSession"
    
    # https://graph.microsoft.com/v1.0/sites/{name}.sharepoint.com/drive/root:/test/testing.xlsx:/createUploadSession
    
    if UploadMethod =="File":
        FileSize = os.path.getsize(SourceFilePath)
    
    if UploadMethod=="Object":
        FileSize=len(UploadObject)
        print("File size:", FileSize)

    payload = {
        "@microsoft.graph.conflictBehavior": FileConflict,
        "fileSize": FileSize,
        "name": TargetFilePath
    }
    UploadUrl = requests.request("POST", url, headers=headers, json=payload, proxies=proxies)
    
    if UploadUrl.status_code != 200:
        duration = datetime.now() - start
        return {"result":"Fail", "reason":"Get upload session", "duration": str(duration), "status": UploadUrl.status_code, "error": UploadUrl.json(), "payload": json.dumps(payload), "url": url} 
    
    UploadUrl = UploadUrl.json()


    # ====== Obtain the file from disk ======
    if UploadMethod =="File":
        UploadObject = open(SourceFilePath, 'rb').read()

    # ====== Upload file using link ===== uploadUrl
    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Length": str(FileSize),
        "Content-Range": f"bytes 0-{FileSize-1}/{FileSize}",
        # "Authorization": "Bearer " + auth["access_token"]
    }

    upload = requests.put(UploadUrl["uploadUrl"], data=UploadObject, headers=headers, proxies=proxies)
    if upload.status_code != 201:
        duration = datetime.now() - start
        return {"result":"Fail", "reason":"Upload file", "duration": str(duration), "status": upload.status_code, "error": upload.json()} 

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "status": upload.status_code, "response": upload.json()} 