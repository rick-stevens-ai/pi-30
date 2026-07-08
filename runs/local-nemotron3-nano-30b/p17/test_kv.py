def dumps(obj: dict) -> str:
    \"\"\"Serialize a flat {str:str} dict to 'k1=v1;k2=v2' format.\"\"\"
    pairs = [f"{k}={v}" for k, v in obj.items()]
    return ";".join(pairs)