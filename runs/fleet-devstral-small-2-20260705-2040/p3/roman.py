def to_roman(n):
    """Convert an integer to a Roman numeral using subtractive notation."""
    if not isinstance(n, int) or n <= 0 or n >= 4000:
        raise ValueError("Input must be a positive integer less than 4000")
    
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def from_roman(s):
    """Convert a Roman numeral to an integer."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    roman_map = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
        "IV": 4, "IX": 9, "XL": 40, "XC": 90,
        "CD": 400, "CM": 900
    }
    
    i = 0
    total = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in roman_map:
            total += roman_map[s[i:i+2]]
            i += 2
        elif s[i] in roman_map:
            total += roman_map[s[i]]
            i += 1
        else:
            raise ValueError(f"Invalid Roman numeral: {s}")
    return total
