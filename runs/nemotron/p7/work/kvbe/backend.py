"""Key-value backend: parse 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}"""


def parse(text: str) -> dict:
    """Parse 'k1=v1;k2=v2' into {'k1': 'v1', 'k2': 'v2'}."""
    if not text:
        return {}
    result = {}
    for pair in text.split(';'):
        if not pair:
            continue
        if '=' not in pair:
            continue
        k, v = pair.split('=', 1)
        result[k] = v
    return result


if __name__ == "__main__":
    # Quick test
    print(parse("k1=v1;k2=v2"))
    print(parse(""))
    print(parse("a=b;c=d;e=f"))
