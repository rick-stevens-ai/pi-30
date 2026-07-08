def dumps(obj: dict) -> str:
    """Dumps a flat {str:str} dict into 'k1=v1;k2=v2' format."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict:
    """Loads a 'k1=v1;k2=v2' string into a flat {str:str} dict."""
    if not s:
        return {}
    return dict(item.split("=", 1) for item in s.split(";") if "=" in item)
