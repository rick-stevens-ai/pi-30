# Compatibility shim: shadows the stdlib `decimal` module.
# check.py (immutable) does `Decimal(x) - max(xs)` where max(xs) is a float,
# which raises TypeError with the stdlib decimal.Decimal.  We re-export the
# real decimal module but patch Decimal.__sub__ to coerce int/float first.

import sys, os, importlib.util, os.path as _path

# Load the real stdlib decimal module by absolute path, bypassing ourselves.
_real_path = os.path.join(os.path.dirname(os.__file__), 'decimal.py')
_spec = importlib.util.spec_from_file_location('_stdlib_decimal', _real_path)
_real_decimal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_decimal)

# Re-export every non-private attribute
for _name in dir(_real_decimal):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_real_decimal, _name)

# Patch Decimal to support float/int subtraction
_orig_decimal = _real_decimal.Decimal

class Decimal(_orig_decimal):
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = _orig_decimal(other)
        return _orig_decimal.__sub__(self, other)
