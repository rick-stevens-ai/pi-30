def parse(s):
    pos = 0

    def skip_whitespace():
        nonlocal pos
        while pos < len(s) and s[pos].isspace():
            pos += 1

    def parse_value():
        nonlocal pos
        skip_whitespace()
        if pos >= len(s):
            raise ValueError("Unexpected end of input")

        char = s[pos]
        if char == '{':
            return parse_object()
        elif char == '[':
            return parse_array()
        elif char == '"':
            return parse_string()
        elif char == 't':
            return parse_literal("true", True)
        elif char == 'f':
            return parse_literal("false", False)
        elif char == 'n':
            return parse_literal("null", None)
        elif char == '-' or char.isdigit():
            return parse_number()
        else:
            raise ValueError(f"Unexpected character {char} at position {pos}")

    def parse_literal(literal, value):
        nonlocal pos
        if s[pos : pos + len(literal)] == literal:
            pos += len(literal)
            return value
        else:
            raise ValueError(f"Expected {literal} at position {pos}")

    def parse_string():
        nonlocal pos
        pos += 1  # Skip opening quote
        start = pos
        while pos < len(s) and s[pos] != '"':
            if s[pos] == '\\':
                pos += 2 # Simple escape handling: skip the backslash and the next char
            else:
                pos += 1
        if pos >= len(s):
            raise ValueError("Unterminated string")
        res = s[start : pos]
        # Handle common escapes if necessary, but for a "subset" maybe just basics.
        # The prompt doesn't specify escape sequences, but JSON usually has them.
        # For now, I'll do basic replacement of \" and \\.
        res = res.replace('\\"', '"').replace('\\\\', '\\')
        pos += 1  # Skip closing quote
        return res

    def parse_number():
        nonlocal pos
        start = pos
        if s[pos] == '-':
            pos += 1
        while pos < len(s) and (s[pos].isdigit() or s[pos] == '.'):
            pos += 1
        num_str = s[start:pos]
        if '.' in num_str:
            return float(num_str)
        else:
            return int(num_str)

    def parse_array():
        nonlocal pos
        pos += 1  # Skip '['
        res = []
        skip_whitespace()
        if pos < len(s) and s[pos] == ']':
            pos += 1
            return res
        while True:
            res.append(parse_value())
            skip_whitespace()
            if pos < len(s) and s[pos] == ',':
                pos += 1
                skip_whitespace()
            elif pos < len(s) and s[pos] == ']':
                pos += 1
                return res
            else:
                raise ValueError("Expected ',' or ']' in array")

    def parse_object():
        nonlocal pos
        pos += 1  # Skip '{'
        res = {}
        skip_whitespace()
        if pos < len(s) and s[pos] == '}':
            pos += 1
            return res
        while True:
            skip_whitespace()
            if pos >= len(s) or s[pos] != '"':
                raise ValueError("Expected string key in object")
            key = parse_string()
            skip_whitespace()
            if pos >= len(s) or s[pos] != ':':
                raise ValueError("Expected ':' after key in object")
            pos += 1  # Skip ':'
            val = parse_value()
            res[key] = val
            skip_whitespace()
            if pos < len(s) and s[pos] == ',':
                pos += 1
                skip_whitespace()
            elif pos < len(s) and s[pos] == '}':
                pos += 1
                return res
            else:
                raise ValueError("Expected ',' or '}' in object")

    result = parse_value()
    skip_whitespace()
    if pos < len(s):
        raise ValueError("Trailing data after JSON value")
    return result
