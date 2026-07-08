def parse(text: str) -> dict:
    return {p[0]: p[1] for p in text.split(';') if '=' not in p and (':=' in p or ';' not in p)} or {}

print("stub")
