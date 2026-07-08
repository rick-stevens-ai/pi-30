"""Base conversion utilities.

This module provides two functions:

* :func:`to_base(n, base)` – Convert an integer ``n`` to a base ``base`` string.
* :func:`parse_int(s, base)` – Parse a base ``base`` string back to an integer.

All conversions are case‑insensitive, but :func:`to_base` outputs
lower‑case strings as required by the exercise. Negatives and ``0``
are correctly handled.
"""

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _validate_base(base: int) -> None:
    """Raise an exception if a base is out of bounds.

    The exercise specifies support for bases 2 through 36 inclusive.
    ``base`` must be an integer; otherwise a :class:`TypeError` is
    raised. If the base does not fall into the allowed range a
    :class:`ValueError` is raised.
    """
    if not isinstance(base, int):
        raise TypeError("base must be an integer")
    if base < 2 or base > 36:
        raise ValueError("base must be between 2 and 36 inclusive")


def to_base(n: int, base: int) -> str:
    """Return the base ``base`` representation of integer ``n``.

    Parameters
    ----------
    n:
        The integer to convert. ``n`` may be negative.
    base:
        Target base – an integer in *[2, 36]*.

    Returns
    -------
    str
        Lower‑case string representing ``n`` in the specified base.
    """
    _validate_base(base)
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    digits = []
    while n:
        n, rem = divmod(n, base)
        digits.append(_DIGITS[rem])
    return sign + "".join(reversed(digits))


def parse_int(s: str, base: int) -> int:
    """Parse a base ``base`` string ``s`` into an integer.

    The function accepts a string with an optional leading ``+`` or ``-``
    and any mixture of lower‑ or upper‑case characters. It raises a
    :class:`ValueError` if the string contains characters not valid for
    the given base.
    """
    _validate_base(base)
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    s = s.strip()
    if not s:
        raise ValueError("empty string")
    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:]
    if s == "":
        raise ValueError("sign only string")
    s = s.lower()
    if s == "0":
        return 0
    value = 0
    for ch in s:
        if ch not in _DIGITS:
            raise ValueError(f"invalid character {ch!r} for base {base}")
        digit = _DIGITS.index(ch)
        if digit >= base:
            raise ValueError(f"digit {ch!r} out of range for base {base}")
        value = value * base + digit
    return sign * value
