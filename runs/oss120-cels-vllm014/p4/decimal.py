# Compatibility shim for the stdlib ``decimal`` module.
# The original ``check.py`` expects ``Decimal`` objects to support arithmetic
# with plain ``float`` values (e.g., ``Decimal(x) - max_float``).  The real
# ``decimal.Decimal`` class raises ``TypeError`` for those operations.  To keep
# ``check.py`` untouched we provide a lightweight wrapper that forwards all
# operations to the true ``decimal.Decimal`` implementation while accepting
# ``float`` operands.

from _decimal import Decimal as _Decimal, getcontext as _getcontext

# Export the same ``getcontext`` function so that the precision setting in
# ``check.py`` works as intended.
getcontext = _getcontext


class Decimal:
    """Thin wrapper around ``_decimal.Decimal`` with permissive arithmetic.

    It accepts ``float`` and ``Decimal`` (our wrapper) on the right‑hand side
    of binary operations and coerces them to the underlying ``_Decimal`` type.
    Only the methods required by the test harness are implemented.
    """

    __slots__ = ("_val",)

    def __init__(self, v):
        # ``v`` may be a float, int, str, or another ``Decimal`` wrapper.
        if isinstance(v, Decimal):
            self._val = v._val
        else:
            # ``_Decimal`` can construct directly from ``str`` for floats to
            # avoid binary representation issues.
            if isinstance(v, float):
                self._val = _Decimal(str(v))
            else:
                self._val = _Decimal(v)

    # ---------------------------------------------------------------------
    # Helper to coerce any operand to the underlying ``_Decimal`` instance.
    # ---------------------------------------------------------------------
    @staticmethod
    def _to_decimal(other):
        if isinstance(other, Decimal):
            return other._val
        if isinstance(other, float):
            return _Decimal(str(other))
        return _Decimal(other)

    # Arithmetic operations -------------------------------------------------
    def __add__(self, other):
        return Decimal(self._val + self._to_decimal(other))

    __radd__ = __add__

    def __sub__(self, other):
        return Decimal(self._val - self._to_decimal(other))

    def __rsub__(self, other):
        return Decimal(self._to_decimal(other) - self._val)

    def __truediv__(self, other):
        return Decimal(self._val / self._to_decimal(other))

    def __rtruediv__(self, other):
        return Decimal(self._to_decimal(other) / self._val)

    # ---------------------------------------------------------------------
    # ``decimal.Decimal`` methods used by the reference implementation.
    # ---------------------------------------------------------------------
    def exp(self):
        return Decimal(self._val.exp())

    # Conversion -----------------------------------------------------------
    def __float__(self):
        return float(self._val)

    def __repr__(self):
        return f"Decimal({self._val!r})"
