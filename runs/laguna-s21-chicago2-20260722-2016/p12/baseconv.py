_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"
    neg = n < 0
    if neg:
        n = -n
    out = []
    while n > 0:
        n, r = divmod(n, base)
        out.append(_DIGITS[r])
    if neg:
        out.append("-")
    return "".join(reversed(out))


def parse_int(s, base):
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    s = s.strip()
    neg = False
    if s and s[0] in "+-":
        neg = s[0] == "-"
        s = s[1:]
    result = 0
    for ch in s:
        val = _DIGITS.find(ch.lower())
        if val == -1 or val >= base:
            raise ValueError(f"invalid digit {ch!r} for base {base}")
        result = result * base + val
    return -result if neg else result