# P13 SEED: only parses a bare integer. No recursion, no other types.
# Updated implementation: full JSON subset parser without using json or eval.

def parse(s):
    """Parse a JSON subset string and return the corresponding Python object.

    Supported literals: null, true, false, numbers (int and float), strings (double‑quoted,
    without escape handling), arrays, objects, and arbitrary whitespace.
    """
    # Use a simple recursive‑descent parser with an index pointer.
    i = 0
    n = len(s)

    def skip_ws():
        nonlocal i
        while i < n and s[i].isspace():
            i += 1

    def parse_value():
        skip_ws()
        if i >= n:
            raise ValueError("Unexpected end of input")
        ch = s[i]
        if ch == 'n':
            return parse_null()
        if ch == 't':
            return parse_true()
        if ch == 'f':
            return parse_false()
        if ch == '"':
            return parse_string()
        if ch == '[':
            return parse_array()
        if ch == '{':
            return parse_object()
        # Number (could start with - or digit)
        if ch == '-' or ch.isdigit():
            return parse_number()
        raise ValueError(f"Unexpected character {ch!r} at position {i}")

    def parse_null():
        nonlocal i
        if s[i:i+4] != 'null':
            raise ValueError('Invalid token, expected null')
        i += 4
        return None

    def parse_true():
        nonlocal i
        if s[i:i+4] != 'true':
            raise ValueError('Invalid token, expected true')
        i += 4
        return True

    def parse_false():
        nonlocal i
        if s[i:i+5] != 'false':
            raise ValueError('Invalid token, expected false')
        i += 5
        return False

    def parse_string():
        nonlocal i
        if s[i] != '"':
            raise ValueError('String must start with a double quote')
        i += 1  # skip opening quote
        start = i
        while i < n and s[i] != '"':
            # Simple implementation: we do not handle escape sequences.
            i += 1
        if i >= n:
            raise ValueError('Unterminated string literal')
        result = s[start:i]
        i += 1  # skip closing quote
        return result

    def parse_number():
        nonlocal i
        start = i
        # optional sign
        if s[i] == '-':
            i += 1
            if i >= n or not s[i].isdigit():
                raise ValueError('Invalid number format')
        # integer part
        while i < n and s[i].isdigit():
            i += 1
        # fractional part
        if i < n and s[i] == '.':
            i += 1
            if i >= n or not s[i].isdigit():
                raise ValueError('Invalid float format')
            while i < n and s[i].isdigit():
                i += 1
            num_str = s[start:i]
            return float(num_str)
        else:
            num_str = s[start:i]
            return int(num_str)

    def parse_array():
        nonlocal i
        if s[i] != '[':
            raise ValueError('Array must start with [')
        i += 1
        skip_ws()
        arr = []
        if i < n and s[i] == ']':
            i += 1
            return arr
        while True:
            arr.append(parse_value())
            skip_ws()
            if i < n and s[i] == ',':
                i += 1
                skip_ws()
                continue
            if i < n and s[i] == ']':
                i += 1
                break
            raise ValueError('Expected , or ] in array')
        return arr

    def parse_object():
        nonlocal i
        if s[i] != '{':
            raise ValueError('Object must start with {')
        i += 1
        skip_ws()
        obj = {}
        if i < n and s[i] == '}':
            i += 1
            return obj
        while True:
            # keys are strings
            if i >= n or s[i] != '"':
                raise ValueError('Object keys must be strings')
            key = parse_string()
            skip_ws()
            if i >= n or s[i] != ':':
                raise ValueError('Expected : after object key')
            i += 1
            skip_ws()
            value = parse_value()
            obj[key] = value
            skip_ws()
            if i < n and s[i] == ',':
                i += 1
                skip_ws()
                continue
            if i < n and s[i] == '}':
                i += 1
                break
            raise ValueError('Expected , or } in object')
        return obj

    result = parse_value()
    skip_ws()
    if i != n:
        raise ValueError('Extra data after valid JSON value')
    return result

