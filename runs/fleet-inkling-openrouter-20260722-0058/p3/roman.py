def to_roman(num):
    val = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'),
        (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'),
        (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    res = ''
    for v, s in val:
        while num >= v:
            res += s
            num -= v
    return res

def from_roman(s):
    mapping = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    res = 0
    i = 0
    while i < len(s):
        if i + 1 < len(s) and mapping[s[i]] < mapping[s[i+1]]:
            res += mapping[s[i+1]] - mapping[s[i]]
            i += 2
        else:
            res += mapping[s[i]]
            i += 1
    return res
