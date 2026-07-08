def to_roman(n):
    if not (0 < n < 4000):
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = n // ints[i]
        result.append(nums[i] * count)
        n -= ints[i] * count
    return ''.join(result)

def from_roman(s):
    if not s:
        raise ValueError("Input cannot be empty")
    s = s.upper()
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
                      'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    i = 0
    num = 0
    while i < len(s):
        # Check for two-character numerals first
        if i+1 < len(s) and s[i:i+2] in roman_numerals:
            num += roman_numerals[s[i:i+2]]
            i += 2
        elif s[i] in roman_numerals:
            num += roman_numerals[s[i]]
            i += 1
        else:
            raise ValueError(f'Invalid Roman numeral character: {s[i]}')
    # Optionally, we can validate that the numeral is in the correct form (e.g., no more than three consecutive same symbols, etc.)
    # But the round-trip test will catch invalid forms.
    return num
