"""Aggregation stage

Provides ``agg`` function that computes basic statistics over a sequence of
numeric values. This follows the specification in ``PLAN.md``:

* ``agg(nums)`` returns a ``dict`` with keys ``count``, ``sum``, ``mean``,
  ``min`` and ``max``.
* All values are plain ``int``/``float`` objects.
* The function works with any iterable of numbers (floats, ints, etc.).
* If the input is empty, ``count`` is ``0`` and the other statistics are set to
  ``0.0`` – a sensible default that keeps the result JSON‑serialisable and
  avoids ``ZeroDivisionError``.

Only the Python standard library is used.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Dict, Any


def agg(nums: Iterable[float]) -> Dict[str, Any]:
    """Return basic aggregation statistics for *nums*.

    Parameters
    ----------
    nums:
        An iterable of numeric values (ints, floats, etc.).  The iterable is
        consumed exactly once.

    Returns
    -------
    dict
        ``{"count": int, "sum": float, "mean": float, "min": float,
        "max": float}``
        For an empty *nums* the numeric fields are ``0.0`` and ``count`` is
        ``0``.
    """
    # Convert to list once so we can reuse for multiple calculations without
    # exhausting a generator.
    values = list(nums)
    count = len(values)
    if count == 0:
        # Empty input – return zeroed statistics.
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}

    total = sum(values)
    mean = total / count
    minimum = min(values)
    maximum = max(values)
    return {
        "count": count,
        "sum": float(total),
        "mean": float(mean),
        "min": float(minimum),
        "max": float(maximum),
    }
