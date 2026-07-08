def dispatch(kind: str, text: str) -> dict:
    """
    Dispatches the request to the appropriate backend based on the kind.

    Args:
        kind: The type of data format ('csv', 'kv', or 'json').
        text: The input text to be parsed.

    Returns:
        A dictionary result from the parsed data.

    Raises:
        ValueError: If the specified kind is not supported.
    """
    backend_map = {
        "csv": "work.csv.backend",
        "kv": "work.kv.backend",
        "json": "work.json.backend",
    }

    if kind not in backend_map:
        raise ValueError(f"Unsupported kind: {kind}. Supported kinds are: {list(backend_map.keys())}")

    module_path = backend_map[kind]
    try:
        # Dynamically import the specific backend module
        from importlib import import_module
        module = import_module(module_path)
        parser = getattr(module, "parse")
        return parser(text)
    except ImportError as e:
        raise ImportError(f"Could not import backend module {module_path}. Ensure the file exists.") from e
    except AttributeError:
        raise AttributeError(f"Backend module {module_path} does not expose a 'parse' function.")