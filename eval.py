
from decision_pattern.router import decide_route
# (question, correct label) - add your own too
TESTS = [
    ("What does len() return?", "simple"),
    ("What is a variable?", "simple"),
    ("How do I print text in Python?", "simple"),
    ("What does the append method do on a list?", "simple"),
    ("What is HTML?", "simple"),
    ("What does SQL stand for?", "simple"),
    ("What is an API?", "simple"),
    ("What is a function in programming?", "simple"),
    ("What does the return keyword do?", "simple"),
    ("What is a boolean?", "simple"),
    ("Explain how a red-black tree stays balanced after insertion and compare it with an AVL tree", "hard"),
    ("Design a rate limiter for a distributed system and discuss the trade-offs", "hard"),
    ("Write a thread-safe LRU cache in Java and explain its time complexity", "hard"),
    ("Compare optimistic and pessimistic locking in database transactions and when to use each", "hard"),
    ("How would you design a URL shortener that handles 100 million requests per day?", "hard"),
    ("Explain how garbage collection works in the JVM and how to tune it for low latency", "hard"),
    ("Explain why Dijkstra's algorithm fails with negative edge weights and suggest alternatives", "hard"),
    ("Walk through implementing B-tree insertion with node splitting in C++", "hard"),
    ("Compare REST, GraphQL and gRPC for a microservice architecture and discuss trade-offs", "hard"),
    ("Explain how the Raft consensus algorithm handles leader election and network partitions", "hard"),
]

rows = []
for q, label in TESTS:
    r = decide_route(q)
    ok = r["choice"] == label
    rows.append((q, label, r, ok))
    print(f"{'OK ' if ok else 'BAD'} | want {label:6} got {r['choice']:6} | conf {r['confidence']:.2f} | {q[:50]}")

total = len(rows)
correct = sum(ok for *_, ok in rows)
confident = [x for x in rows if x[2]["confidence"] >= 0.8]
conf_correct = sum(x[3] for x in confident)
to_small = sum(1 for x in rows if x[2]["route"] == "small")
hard_to_small = sum(1 for q, label, r, ok in rows if label == "hard" and r["route"] == "small")

print("\n--- Summary ---")
print(f"Overall accuracy: {correct}/{total}")
print(f"Confident (>=0.8) decisions: {len(confident)}, of which correct: {conf_correct}")
print(f"Routed to small model: {to_small}/{total}")
print(f"Hard questions wrongly sent to small model: {hard_to_small}")