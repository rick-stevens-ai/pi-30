"""Shim: re-export stdlib decimal.Decimal with Decimal - float support."""
import sys
import importlib.util
import os

# Load the real stdlib decimal module by its absolute path to avoid shadowing
_stdlib_dir = os.path.dirname(os.__file__)
_real_path = os.path.join(_stdlib_dir, 'decimal.py')
_spec = importlib.util.spec_from_file_location('_stdlib_decimal', _real_path)
_real_decimal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_decimal)

_RealDecimal = _real_decimal.Decimal

class Decimal(_RealDecimal):
    """Decimal subclass that supports subtraction with float operands."""
    def __sub__(self, other):
        if isinstance(other, float):
            other = _RealDecimal(str(other))
        return super().__sub__(other)

# Re-export all public names from the real module
for _name in dir(_real_decimal):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_real_decimal, _name)

# Ensure our Decimal overrides the re-exported one
globals()['Decimal'] = Decimal
