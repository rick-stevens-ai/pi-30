def dumps(obj: dict[str, str]) -> str:
    """Dumps a flat {str: str} dictionary to a string in 'k1=v1;k2=v2' format."""
    return ";".join(f"{k}={v}" for k, v in obj.items())

def loads(s: str) -> dict[str, str]:
    """Loads a 'k1=v1;k2=v2' formatted string into a {str: str} dictionary."""
    if not s:
        return {}
    return dict(part.split("=", 1) for part in s.split(";") if part)
