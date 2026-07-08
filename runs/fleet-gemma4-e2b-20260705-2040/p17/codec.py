from importlib import import_module

def round_trip(fmt, obj):
    """
    Performs a round trip operation using the specified format's backend.
    It calls dumps from work/<fmt>/backend.py and then loads the result using loads.
    """
    module_path = f"work/{fmt}/backend"
    
    try:
        # Dynamically import the backend module
        backend = import_module(module_path)
    except ImportError as e:
        raise ImportError(f"Could not import backend from {module_path}. Ensure '{module_path}' exists.") from e

    if not hasattr(backend, 'dumps') or not hasattr(backend, 'loads'):
        raise AttributeError(f"Backend at {module_path} must expose dumps(obj)->str and loads(s)->obj")

    # Perform round trip: loads(dumps(obj))
    dumped = backend.dumps(obj)
    loaded = backend.loads(dumped)
    return loaded

if __name__ == '__main__':
    # Example usage placeholder, actual verification is done via verify.py
    print("codec.py loaded successfully.")