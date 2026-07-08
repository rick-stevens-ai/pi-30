DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    out = []
    while n > 0:
        out.append(DIGITS[n % base])
        n //= base
    if negative:
        out.append("-")
    return "".join(reversed(out))


def parse_int(s, base):
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    s = s.strip()
    negative = False
    if s and s[0] in "+-":
        negative = s[0] == "-"
        s = s[1:]
    if not s:
        raise ValueError("empty string")
    n = 0
    for ch in s:
        v = DIGITS.index(ch.lower())
        if v >= base:
            raise ValueError(f"invalid digit {ch!r} for base {base}")
        n = n * base + v
    return -n if negative else n
