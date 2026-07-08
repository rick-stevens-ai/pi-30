def to_roman(n):
    """Convert integer to Roman numeral using subtractive notation."""
    if not 0 < n < 4000:
        raise ValueError("Value must be between 1 and 3999")
    
    val_symbols = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]
    
    result = []
    for value, symbol in val_symbols:
        while n >= value:
            result.append(symbol)
            n -= value
    return ''.join(result)


def from_roman(s):
    """Convert Roman numeral to integer."""
    s = s.upper()
    if not s:
        raise ValueError("Input cannot be empty")
    
    roman_symbols = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman_symbols.get(char, None)
        if value is None:
            raise ValueError(f"Invalid Roman numeral: {char}")
        
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total
