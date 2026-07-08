"""Clean stage for the stats pipeline.

This module provides a single function :func:`clean` which takes an iterable of
values (typically strings) and returns a list of ``float`` values.  Any element
that cannot be converted to a ``float`` – for example ``None`` , empty strings,
or non‑numeric placeholders such as ``"x"`` – is silently dropped.

The implementation is deliberately minimal and uses only the Python standard
library.
"""

from __future__ import annotations

from typing import Iterable, List

__all__ = ["clean"]


def clean(rows: Iterable[object]) -> List[float]:
    """Return a list of floats extracted from *rows*.

    Parameters
    ----------
    rows:
        An iterable containing values that may or may not be convertible to
        ``float``.  Elements can be of any type; the function attempts to cast
        each element using ``float()``.

    Returns
    -------
    List[float]
        A new list containing the successfully converted ``float`` values in
        the order they appeared in *rows*.

    Notes
    -----
    Elements that raise ``ValueError`` or ``TypeError`` during conversion are
    ignored.  This includes ``None``, empty strings, and any non‑numeric string
    such as ``"x"``.
    """
    cleaned: List[float] = []
    for element in rows:
        try:
            # ``float`` can handle numbers, numeric strings and ``bool`` (as 0.0
            # or 1.0).  ``bool`` is a subclass of ``int``; converting it is fine.
            # For other types we rely on ``float`` raising an appropriate
            # exception which we then swallow.
            cleaned.append(float(element))
        except (ValueError, TypeError):
            # Silently drop elements that cannot be converted.
            continue
    return cleaned
