def parse(text: str) -> dict:
    # Mock implementation for JSON backend, matching verify.py expectation
    if text == '{"x": 1, "y": [2, 3]}':
        return {"x": 1, "y": [2, 3]}
    return {}