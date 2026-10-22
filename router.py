import json
import urllib.request
import urllib.error

DECIDER_URL = "http://127.0.0.1:8765/v1/systemone"
CONFIDENCE_THRESHOLD = 0.8


def decide_route(question: str) -> dict:
    """Ask Decider whether a question is simple or hard, then pick a route."""
    payload = {
        "state": question,
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
        DECIDER_URL,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )
    reply = json.load(urllib.request.urlopen(req))
    answer = reply["answers"]["difficulty"]
    choice, confidence = answer["choice"], answer["confidence"]

    if choice == "simple" and confidence >= CONFIDENCE_THRESHOLD:
        route, reason = "small", "confident it is simple"
    elif choice == "simple":
        route, reason = "large", "low confidence, playing safe"
    else:
        route, reason = "large", "judged hard"

    return {
        "route": route,
        "choice": choice,
        "confidence": confidence,
        "reason": reason,
     "probabilities": answer["probabilities"],
        "latency_ms": reply["latency_ms"],
    }


if __name__ == "__main__":
    tests = [
        "What does the print function do in Python?",
        "What is a variable?",
        "Explain how a red-black tree stays balanced after insertion and compare it with an AVL tree",
        "Design a rate limiter for a distributed system and discuss the trade-offs",
        "What does len() return?",
    ]
    for q in tests:
        r = decide_route(q)
        print(f"{r['route']:5} | {r['choice']:6} | conf {r['confidence']:.2f} | {r['latency_ms']:.0f} ms | {q[:55]}")