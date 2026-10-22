import os

k = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
print("key is set:", k is not None)
if k:
    print("length:", len(k))
    print("first 4 characters:", k[:4])
    print("has quote mark:", '"' in k or "'" in k)
    print("has space or line break:", any(c.isspace() for c in k))
print("region:", os.environ.get("AWS_DEFAULT_REGION"))
print("old access keys also set:", "AWS_ACCESS_KEY_ID" in os.environ)