import json
import urllib.request

payload = {
    "state": "Help! My payouts have been failing for 3 days!",
    "questions": {
        "is_urgent": {"type": "noul", "instructions": "Does this convey urgency?"}
    },
}

req = urllib.request.Request(
    "http://127.0.0.1:8765/v1/systemone",
    data=json.dumps(payload).encode(),
    headers={"content-type": "application/json"},
)
reply = json.load(urllib.request.urlopen(req))
print(json.dumps(reply, indent=2))