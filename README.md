# Decision Pattern: Confidence-Gated Model Routing

**Pattern:** Model routing (`#model-routing`) with Strands Decider 2B.

Decide whether a question needs a large model or a small one, and use
Decider's confidence score to fall back to the large model when it is unsure.

## The typed question and options

| Field | Value |
|---|---|
| Question type | `choice` |
| Instructions | "How complex is this question?" |
| Options | `simple`: a basic factual or definition question, answerable in a sentence or two |
| | `hard`: needs deep multi-step reasoning, a detailed comparison, or long code |

## The wiring

`router.py` exposes one function, `decide_route(question)`. It sends the question
to a local Decider server (`/v1/systemone`), reads the choice and confidence, and
returns a route:

- `simple` with confidence >= `CONFIDENCE_THRESHOLD` (default 0.8) -> `small`
- `simple` with lower confidence -> `large` (play safe)
- `hard` -> `large`

Your agent calls it before choosing which Bedrock model answers. See `agent.py`
and `app.py` for two working examples.

## How to use it in your own agent

1. Start the server:
   `strands-decider serve StrandsAgents/strands-decider-2B-hobson-v19 --port 8765 --device cpu`
2. Copy `router.py` into your project.
3. Change the two option descriptions to match your own models and domain.
4. Call `decide_route(user_text)` and send the request to the model it names.
5. Tune `CONFIDENCE_THRESHOLD` using your own labeled questions (see `eval.py`).

## Results from my small test (20 questions, labeled by me)

- Overall accuracy: 18 / 20
- Decisions at confidence >= 0.8: 10, all correct
- Hard questions wrongly sent to the small model: 0
- The two mistakes had low confidence (0.18 and 0.33), so the fallback rule sent them to the large model.

## Limitations

- Experimental model; small, self-labeled test set, so treat the numbers as indicative only.
- High confidence is not a guarantee: [describe the red-black tree example you saw, 0.82 confidence on a casual phrasing].
- On a CPU, a Decider call took about [2] seconds, which is not faster than a Bedrock call. The model's published speed figures assume suitable hardware, which I did not test.
