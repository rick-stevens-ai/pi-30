"""A thin wrapper around the standard :mod:`decimal` module.

This file shadows the standard library ``decimal`` module when
imported from the current working directory. It exposes a
subclass :class:`Decimal` that allows subtraction with ``float``
instances without raising :class:`TypeError`.  The drop‑in
replacement otherwise re‑exports everything from the real
module.
"""

# Import the real module
_from decimal import Decimal as _RealDecimal, getcontext as _getcontext

class Decimal(_RealDecimal):
    """Extended Decimal supporting subtraction from floats.

    The standard :class:`decimal.Decimal` does not allow
    ``Decimal - float``.  This subclass overrides ``__sub__`` and
    ``__rsub__`` to coerce float operands to a :class:`Decimal`
    before delegating to the parent implementation.
    """

    def __sub__(self, other):  # type: ignore[override]
        if isinstance(other, float):
            other = _RealDecimal(other)
        return super().__sub__(other)

    def __rsub__(self, other):  # type: ignore[override]
        if isinstance(other, float):
            other = _RealDecimal(other)
        return _RealDecimal(other) - self

# Restretch the public API to mimic the real module
getcontext = _getcontext
__ laparangan__ = "Decimal, getcontext"
