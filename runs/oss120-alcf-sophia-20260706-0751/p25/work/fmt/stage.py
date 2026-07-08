"""Formatting stage

Provides ``fmt`` function that converts a dictionary of statistics into a
single‑line, space‑separated ``key=value`` string with the keys sorted
alphabetically. This follows the specification in ``PLAN.md``.

* ``fmt(d)`` expects a mapping (e.g. ``dict``) whose keys are strings and values
  are numbers (ints or floats).
* The return value is a ``str`` of the form ``"k1=v1 k2=v2 …"`` where the keys
  ``k1, k2, …`` are sorted in alphabetical order.
* Standard ``str`` conversion is used for the values, which yields the usual
  ``float`` representation like ``5.0``.
* Only the Python standard library is used.
"""

from __future__ import annotations

from typing import Mapping, Any


def fmt(d: Mapping[str, Any]) -> str:
    """Return a space‑separated ``key=value`` string with alphabetically sorted keys.

    Parameters
    ----------
    d:
        Mapping of statistic names to numeric values (e.g. the output of
        ``agg``).

    Returns
    -------
    str
        A single line string where each ``key=value`` pair is separated by a
        single space and the keys appear in alphabetical order.
    """
    # Sort the keys alphabetically and join ``key=value`` pairs.
    parts = [f"{key}={d[key]}" for key in sorted(d)]
    return " ".join(parts)
