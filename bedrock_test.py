import boto3

SMALL_MODEL = "eu.amazon.nova-lite-v1:0"
LARGE_MODEL = "eu.amazon.nova-pro-v1:0"

client = boto3.client("bedrock-runtime", region_name="eu-north-1")

def ask(model_id, question):
    resp = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": question}]}],
    )
    return resp["output"]["message"]["content"][0]["text"]

print(ask(SMALL_MODEL, "In one sentence, what does print() do in Python?"))
print(ask(LARGE_MODEL, "In one sentence, what does print() do in Python?"))