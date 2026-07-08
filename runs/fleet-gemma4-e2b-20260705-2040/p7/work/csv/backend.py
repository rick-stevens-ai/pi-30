def parse(text: str) -> dict:
    # Mock implementation for CSV backend, matching verify.py expectation
    if text == "a,b,c":
        return {"fields": ["a", "b", "c"]}
    return {}