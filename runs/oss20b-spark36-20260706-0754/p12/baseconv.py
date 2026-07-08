# Utility functions for base conversions.

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _check_base(base: int):  # internal helper
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36, inclusive")


def to_base(n: int, base: int) -> str:
    """Return the string representation of integer ``n`` in ``base``.

    Parameters
    ----------
    n : int
        Integer to convert. May be negative.
    base : int
        Base for conversion; must satisfy 2 <= base <= 36.

    Returns
    -------
    str
        Lower‑case representation of ``n`` in the given base, following
        Python's convention: digits ``0-9`` then ``a-z``.

    Examples
    --------
    >>> to_base(255, 16)
    'ff'
    >>> to_base(-10, 2)
    '-1010'

    """
    _check_base(base)
    if n == 0:
        return "0"
    neg = n < 0
    n_abs = -n if neg else n
    digits = []
    while n_abs > 0:
        n_abs, rem = divmod(n_abs, base)
        digits.append(DIGITS[rem])
    s = "".join(reversed(digits))
    return f"-{s}" if neg else s


def parse_int(s: str, base: int) -> int:
    """Parse ``s`` as an integer of the given *base*.

    This function simply delegates to Python's built‑in ``int`` which
    performs validation and handles leading sign characters. It
    therefore matches ``int(s, base)`` exactly and is suitable for
    round‑tripping when using :func:`to_base` above.

    Parameters
    ----------
    s : str
        String representation of integer in the given base;
        may contain a leading ``-`` to denote negativity.
    base : int
        Base of the numeral system; must satisfy 2 <= base <= 36.

    Returns
    -------
    int
        Integer value represented by *s*.

    """
    _check_base(base)
    return int(s, base)
