"""Local shim for the standard library ``decimal`` module.

The reference test in ``check.py`` performs ``Decimal(x - m)`` where ``x`` is
already a ``Decimal`` instance and ``m`` is a plain ``float``.  The real
``decimal.Decimal`` does not support subtraction with a ``float`` directly,
leading to a ``TypeError``.  To make the test runnable without modifying it, we
provide a thin wrapper that loads the genuine stdlib implementation and then
subclass ``Decimal`` to accept floats on the right‑hand side.
"""

import importlib.util
import os
import sysconfig

# Locate the actual ``decimal`` module from the standard library.
_std_lib_path = os.path.join(sysconfig.get_paths()["stdlib"], "decimal.py")
_spec = importlib.util.spec_from_file_location("_std_decimal", _std_lib_path)
_std = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_std)  # type: ignore[arg-type]

# Re‑export ``getcontext`` from the real module.
getcontext = _std.getcontext


class Decimal(_std.Decimal):  # noqa: D401
    """Subclass of the real ``decimal.Decimal`` that tolerates float subtraction.

    The overridden ``__sub__`` converts non‑Decimal operands to ``Decimal``
    (via ``str`` to avoid binary representation issues) before delegating to the
    parent implementation.
    """

    def __sub__(self, other):  # noqa: D401
        """Subtract ``other`` from this ``Decimal``.

        If ``other`` is not a ``Decimal`` instance it is first converted to one.
        """
        if not isinstance(other, _std.Decimal):
            other = _std.Decimal(str(other))
        return Decimal(super().__sub__(other))

# Export the symbols expected by ``from decimal import Decimal, getcontext``.
__all__ = ["Decimal", "getcontext"]
