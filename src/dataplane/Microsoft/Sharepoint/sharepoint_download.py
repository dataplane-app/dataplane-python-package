
import requests
import os
from datetime import datetime
import json

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
def SharepointDownload(Host, TenantID, ClientID, Secret, SiteName, LocalFilePath, SharepointFilePath, ProxyUse=False, ProxyUrl="", ProxyMethod="https"):

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

    # ====== Get Item ID =====

    # Note the target path must have a / prefix
    SharepointFilePath = SharepointFilePath.replace(" ", "%20")
    url = f"https://graph.microsoft.com/v1.0/sites/{SiteID['id']}/drive/root:{SharepointFilePath}"

    
    ItemID = requests.request("GET", url, headers=headers, json=payload, proxies=proxies)
    
    if ItemID.status_code != 200:
        duration = datetime.now() - start
        return {"result":"Fail", "reason":"Get upload session", "duration": str(duration), "status": ItemID.status_code, "error": ItemID.json(), "payload": json.dumps(payload), "url": url} 
    
    ItemID = ItemID.json()


    # ====== Download file using link =====
    r = requests.get(ItemID["@microsoft.graph.downloadUrl"])  
    with open(LocalFilePath, 'wb') as f:
        f.write(r.content)


    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "status": r.status_code, "FilePath": LocalFilePath} 