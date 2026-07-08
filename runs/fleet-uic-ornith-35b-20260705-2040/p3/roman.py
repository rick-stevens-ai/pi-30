_RAN = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'),
]
_IV = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def to_roman(n: int) -> str:
    res = []
    for val, sym in _RAN:
        while n >= val:
            res.append(sym)
            n -= val
    return ''.join(res)

def from_roman(s: str) -> int:
    total = 0
    prev = 0
    for ch in reversed(s):
        v = _IV[ch]
        if v < prev:
            total -= v
        else:
            total += v
        prev = v
    return total
