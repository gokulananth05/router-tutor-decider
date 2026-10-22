import json
import urllib.request
import urllib.error

def ask(state):
    payload = {
        "state": state,
        "questions": {
            "difficulty": {
                "type": "choice",
                "instructions": "How complex is this question?",
                "criteria": {
"simple": "a basic factual or definition question, answerable in a sentence or two",
    "hard": "needs deep multi-step reasoning, a detailed comparison, or long code",
},
            }
        },
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8765/v1/systemone",
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"HTTP_ERROR": e.code, "body": e.read().decode()}

print(json.dumps(ask("What does the print function do in Python?"), indent=2))
print(json.dumps(ask("Explain how a red-black tree stays balanced after insertion and compare it with an AVL tree"), indent=2))