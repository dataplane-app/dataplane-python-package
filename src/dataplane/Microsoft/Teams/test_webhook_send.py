
import os
from .webhook_send import teams_webhook_send
from nanoid import generate
import os
from dotenv import load_dotenv

def test_webhook_send():

    # ---------- DATAPLANE RUN ------------
    
    # Dataplane run id
    os.environ["DP_RUNID"] = generate('1234567890abcdef', 10)

    # Sharepoint connection
    load_dotenv()

    RUN_ID = os.environ["DP_RUNID"]
    WEBHOOK = os.getenv('TEAMS_WEBHOOK')

    CardSend = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "ff5722",
    "summary": "Dataplane Teams Webhook",
    "sections": [{
        "activityTitle": "Dataplane created a new task",
        "activitySubtitle": f"Dataplane Project {RUN_ID}",
        "activityImage": "https://media-exp1.licdn.com/dms/image/C4D03AQEJoeNB6rr56A/profile-displayphoto-shrink_200_200/0/1516479449675?e=2147483647&v=beta&t=juVBAJjtQXXlLw5cWjTFH4M9ztiQyR6PnaKuSIh1_PQ"
    }]
}

    # ---------- Send a webhook ------------

    rs = teams_webhook_send(Url=WEBHOOK, Message=CardSend)
    print(rs)
    assert rs["result"]=="OK"