import json
import time

from strands import Agent
from strands.models import BedrockModel


from decision_pattern.router import decide_route
REGION = "eu-north-1"
SMALL_MODEL = "eu.amazon.nova-lite-v1:0"
LARGE_MODEL = "eu.amazon.nova-pro-v1:0"
SYSTEM_PROMPT = "You are a friendly coding tutor. Keep answers clear and concise."

agents = {
    "small": Agent(
        model=BedrockModel(model_id=SMALL_MODEL, region_name=REGION),
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    ),
    "large": Agent(
        model=BedrockModel(model_id=LARGE_MODEL, region_name=REGION),
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    ),
}


def answer(question: str) -> None:
    decision = decide_route(question)
    print(
        f"\n[Decider] {decision['choice'].upper()} "
        f"(confidence {decision['confidence']:.2f}) -> {decision['route']} model "
        f"| {decision['reason']} | {decision['latency_ms']:.0f} ms"
    )

    start = time.time()
    reply = str(agents[decision["route"]](question))
    elapsed = (time.time() - start) * 1000

    print(f"\n{reply}\n")
    print(f"[Bedrock answered in {elapsed:.0f} ms]")

    with open("decisions.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"question": question, **decision, "bedrock_ms": round(elapsed)}) + "\n")


if __name__ == "__main__":
    print("Smart Router Tutor. Type a question, or 'quit' to exit.")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in ("quit", "exit"):
            break
        if q:
            answer(q)