"""Aggregation stage for the stats pipeline.

Provides a single function ``agg`` that takes an iterable of numbers and
returns a dictionary with basic summary statistics:

* ``count`` – number of items (int)
* ``sum``   – arithmetic sum of the items (float)
* ``mean``  – average value (float)
* ``min``   – smallest value (float)
* ``max``   – largest value (float)

The implementation uses only the Python standard library and works with any
iterable of ``int`` or ``float`` values.  If the input is empty the function
returns a dictionary where ``count`` is ``0`` and the remaining fields are
``0.0`` – this mirrors the behaviour of many CLI tools that report ``0`` for
aggregates on empty input.
"""

from __future__ import annotations
from typing import Iterable, Dict, Any


def agg(nums: Iterable[float]) -> Dict[str, Any]:
    """Aggregate a sequence of numbers.

    Parameters
    ----------
    nums: Iterable[float]
        The numeric values to aggregate.

    Returns
    -------
    dict
        Mapping with keys ``count``, ``sum``, ``mean``, ``min`` and ``max``.
        ``count`` is an ``int``; the other values are ``float``.
    """
    # Convert to list once so we can compute length and reuse values.
    values = list(nums)
    count = len(values)
    if count == 0:
        # Return zeros for an empty input – callers can decide how to handle.
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}

    total = sum(values)
    minimum = min(values)
    maximum = max(values)
    mean = total / count
    return {
        "count": count,
        "sum": float(total),
        "mean": float(mean),
        "min": float(minimum),
        "max": float(maximum),
    }

# The module's public API consists solely of ``agg``.
__all__ = ["agg"]
