import importlib.util
import sys


def round_trip(fmt: str, obj) -> object:
    """Serialize and deserialize obj using the specified backend format."""
    spec = importlib.util.spec_from_file_location("backend", f"work/{fmt}/backend.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"work.{fmt}.backend"] = module
    spec.loader.exec_module(module)
    return module.loads(module.dumps(obj))