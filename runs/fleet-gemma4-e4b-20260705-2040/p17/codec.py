import importlib
from typing import Any, TypeVar

T = TypeVar('T')

def round_trip(fmt: str, obj: T) -> T:
    """
    Performs a round trip encoding and decoding using the specified format backend.
    
    Args:
        fmt: The format identifier (e.g., 'csv', 'kv', 'pylit').
        obj: The object to serialize and deserialize.

    Returns:
        The deserialized object.

    Raises:
        ImportError: If the specified format backend cannot be imported.
    """
    try:
        module_name = f"work.{fmt}.backend"
        backend = importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Could not load backend for format '{fmt}'. Check if 'work/{fmt}/backend.py' exists. Error: {e}")

    # Ensure the module has dumps and loads functions
    if not hasattr(backend, 'dumps') or not callable(getattr(backend, 'dumps')):
        raise AttributeError(f"Backend in work.{fmt}.backend does not have a 'dumps' function.")
    if not hasattr(backend, 'loads') or not callable(getattr(backend, 'loads')):
        raise AttributeError(f"Backend in work.{fmt}.backend does not have a 'loads' function.")

    # 1. Dump the object to string
    serialized_data = backend.dumps(obj)
    
    # 2. Load the string back into an object
    deserialized_obj = backend.loads(serialized_data)
    
    return deserialized_obj

if __name__ == '__main__':
    # Example usage (assuming some dummy objects for testing if needed, but main focus is on round_trip function)
    print("Codec loaded successfully.")