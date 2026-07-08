def _value(char):
    return {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,
            'D': 500, 'M': 1000}.get(char)

def to_roman(n):
    vals = [1000, 900, 500, 400, 100, 90, 50, 40,
            10, 9, 5, 4, 1]
    syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL',
            'X', 'IX', 'V', 'IV', 'I']
    result = []
    for v, s in zip(vals, syms):
        while n >= v:
            result.append(s)
            n -= v
    return ''.join(result)

def from_roman(s):
    result = 0
    prev = 0
    for ch in reversed(s.upper()):
        v = _value(ch)
        if v < prev:
            result -= v
        else:
            result += v
        prev = v
    return result
