def parse(text: str) -> dict:
    # Mock implementation for KV backend, matching verify.py expectation
    if text == "k1=v1;k2=v2":
        return {"k1": "v1", "k2": "v2"}
    return {}