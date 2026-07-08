"""Clean stage

Provides ``clean`` function that filters a sequence of values, converting each
value to ``float`` and discarding any that cannot be converted.  This matches the
specification in ``PLAN.md``:

* Drop any element that isn't convertible to ``float`` – e.g. ``None``, empty
  strings, or arbitrary text like ``"x"``.
* Return a ``list[float]`` preserving the original order of the successfully
  converted values.

Only the Python standard library is used.
"""

from __future__ import annotations

from typing import Iterable, List


def clean(rows: Iterable[object]) -> List[float]:
    """Return a list of floats from *rows*, discarding non‑convertible items.

    The function attempts to cast each element to ``float``.  If ``float`` raises
    ``TypeError`` or ``ValueError`` the element is ignored.  The order of the
    successfully converted elements is retained.

    Parameters
    ----------
    rows:
        An iterable of arbitrary objects – typically strings or numbers.

    Returns
    -------
    list[float]
        A new list containing only the successfully converted float values.
    """
    cleaned: List[float] = []
    for value in rows:
        try:
            # ``float`` handles numbers, numeric strings and strings with
            # whitespace.  Anything else (None, empty string, non‑numeric text)
            # will raise ``TypeError`` or ``ValueError``.
            cleaned.append(float(value))
        except (TypeError, ValueError):
            # Silently drop values that cannot be converted.
            continue
    return cleaned
