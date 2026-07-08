"""Dispatch module: route parse requests to the appropriate backend."""
from csvbe.backend import parse as csv_parse
from jsonbe.backend import parse as json_parse
from kvbe.backend import parse as kv_parse


_BACKENDS = {
    "csv": csv_parse,
    "json": json_parse,
    "kv": kv_parse,
}


def dispatch(format_name: str, text: str) -> dict:
    """
    Parse text using the specified format backend.

    Args:
        format_name: One of "csv", "json", "kv"
        text: Input text to parse

    Returns:
        Parsed result as a dict

    Raises:
        ValueError: If format_name is not recognized
    """
    if format_name not in _BACKENDS:
        raise ValueError(f"Unknown format: {format_name!r}. Supported: {list(_BACKENDS.keys())}")
    return _BACKENDS[format_name](text)


# Alias for backwards compatibility
parse = dispatch


def available_formats() -> list[str]:
    """Return list of supported format names."""
    return list(_BACKENDS.keys())


if __name__ == "__main__":
    # Quick test
    print("Available formats:", available_formats())
    print("CSV:", parse("csv", "a,b,c"))
    print("JSON:", parse("json", '{"a": 1, "b": 2}'))
    print("KV:", parse("kv", "k1=v1;k2=v2"))
    try:
        parse("unknown", "data")
    except ValueError as e:
        print("Expected error:", e)