def to_base(n, base):
    """Convert integer n to a lowercase string in the given base (2-36)."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    res = []
    while n > 0:
        res.append(digits[n % base])
        n //= base
    if negative:
        return "-" + "".join(reversed(res))
    else:
        return "".join(reversed(res))


def parse_int(s, base):
    """Parse a string s in the given base (2-36) to an integer.
    Matches int(s, base) behavior for valid inputs."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    s = s.strip()
    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]

    # Allow "0" or strings that become empty after stripping zeros
    s = s.lstrip("0") or "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    value = 0
    for ch in s:
        val = digits.index(ch.lower())
        if not 0 <= val < base:
            raise ValueError(f"invalid digit '{ch}' for base {base}")
        value = value * base + val
    return sign * value