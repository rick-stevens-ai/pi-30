# Custom decimal module that patches the Decimal class to allow subtraction with floats.
# This file is placed in the project root so it shadows stdlib's decimal when
# imported. It exposes ``Decimal`` (the patched subclass) and re‑exports
# ``getcontext`` unchanged for compatibility.

import importlib.util
import importlib.machinery
import sysconfig
# Load stdlib decimal module avoiding circular import due to local file name
def _load_std_decimal():
    stdlib_dir = sysconfig.get_path('stdlib')
    spec = importlib.machinery.PathFinder.find_spec('decimal', [stdlib_dir])
    _std_decimal_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_std_decimal_mod)
    return _std_decimal_mod.Decimal, _std_decimal_mod.getcontext

_StdDecimal, _getcontext = _load_std_decimal()


class Decimal(_StdDecimal):
    """A Drop‑in replacement for stdlib.Decimal with float subtraction support."""
    def __sub__(self, other):
        try:
            return super().__sub__(other)
        except Exception:
            # ``other`` might be a float – convert it to Decimal first.
            return super().__sub__(_StdDecimal(other))

# Re‑export the original getcontext under its usual name.
getcontext = _getcontext
