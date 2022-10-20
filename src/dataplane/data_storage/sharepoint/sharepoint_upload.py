
import requests
from datetime import datetime

""" Host: {name}.sharepoint.com 
TenantID: Directory or TenantID as per Azure portal
ClientID: Azure Client ID or Application ID.
Secret: Azure secret for client ID.
SiteName: Name of the site to be looked up

ProxyUse: Whether to use a proxy, true or false
ProxyUrl: Proxy endpoint to use
ProxyMethod: https or http, default https
"""
def SharepointUpload(Host, TenantID, ClientID, Secret, SiteName, ProxyUse=False, ProxyUrl="", ProxyMethod="https"):

    # Start the timer
    start  = datetime.now()

    # Authenticate with Sharepoint

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
        return {"result":"Fail", "duration": str(duration), "error": auth.text, "status": auth.status_code} 


    auth = auth.json()

    # Get the site ID from the site name
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }
    SiteName = SiteName.replace(" ", "")
    url = f"https://graph.microsoft.com/v1.0/sites/{Host}:/sites/{SiteName}"
    

    SiteID = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)
    
    if SiteID.status_code != 200:
        duration = datetime.now() - start
        return {"result":"Fail", "duration": str(duration), "error": SiteID.text, "status": SiteID.status_code} 
    
    SiteID = SiteID.json()
    # Create an upload session
    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration), "SiteID": SiteID["id"]} 