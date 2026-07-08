def to_roman(n):
    val = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
           (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
           (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = ''
    for v, s in val:
        while n >= v:
            result += s
            n -= v
    return result

def from_roman(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        v = vals[s[i]]
        if i + 1 < len(s) and v < vals[s[i+1]]:
            total -= v
        else:
            total += v
    return total
