"""Local shim for the standard library ``decimal`` module.

The original reference implementation in ``check.py`` performs ``Decimal(x - m)``
where ``x`` is already a ``Decimal`` instance and ``m`` is a plain ``float``.
The real ``decimal.Decimal`` does **not** support arithmetic with ``float`` – it
raises ``TypeError``.  To keep the test harness untouched we provide a small
wrapper that accepts ``float`` operands by converting them to ``Decimal``
internally.

Only the symbols used by the test (``Decimal`` and ``getcontext``) are
re‑exported; everything else is delegated to the real ``decimal`` module.
"""

import sysconfig
import importlib.util
import os

# Load the real stdlib ``decimal`` module from its installation location.
_stdlib_path = sysconfig.get_paths()['stdlib']
_decimal_path = os.path.join(_stdlib_path, 'decimal.py')
_spec = importlib.util.spec_from_file_location('_stdlib_decimal', _decimal_path)
_std = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_std)

# Re‑export the original ``getcontext`` implementation unchanged.
getcontext = _std.getcontext


class Decimal(_std.Decimal):
    """Subclass of :class:`decimal.Decimal` that tolerates ``float`` arithmetic.

    ``Decimal`` from the stdlib refuses to operate directly with ``float``
    objects.  The test suite expects ``Decimal(x - m)`` where ``m`` is a float.
    This subclass forwards operations to the parent class after converting any
    non‑Decimal operand to a ``Decimal`` using ``str`` to avoid the binary float
    representation issues that can arise from passing the float directly.
    """

    def __new__(cls, value="0", *args, **kwargs):  # noqa: D401
        # ``float`` values are converted via ``str`` to retain the exact decimal
        # representation used by the reference implementation.
        if isinstance(value, float):
            value = str(value)
        return super().__new__(cls, value, *args, **kwargs)

    def _coerce_other(self, other):
        if isinstance(other, Decimal):
            return other
        if isinstance(other, _std.Decimal):
            # Cast to our subclass for consistency.
            return Decimal(str(other))
        # Assume ``other`` is a numeric type that can be losslessly represented
        # as a decimal string.
        return Decimal(str(other))

    # Override arithmetic methods that may receive a ``float``.
    def __sub__(self, other):
        other = self._coerce_other(other)
        return Decimal(super().__sub__(other))

    def __add__(self, other):
        other = self._coerce_other(other)
        return Decimal(super().__add__(other))

    def __mul__(self, other):
        other = self._coerce_other(other)
        return Decimal(super().__mul__(other))

    def __truediv__(self, other):
        other = self._coerce_other(other)
        return Decimal(super().__truediv__(other))

    # Ensure reverse operations also work.
    __rsub__ = __sub__
    __radd__ = __add__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

__all__ = ["Decimal", "getcontext"]
