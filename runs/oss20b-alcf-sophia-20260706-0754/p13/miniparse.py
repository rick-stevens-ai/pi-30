# P13 iterate-until-green: a tiny JSON-subset parser (no eval, no json module).
# Supports null/true/false, ints, floats, strings, arrays, objects, nesting,
# whitespace.

import re

# Regex for a number as per JSON spec: optional sign, digits, optional fraction, optional exponent.
_number_re = re.compile(r'^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?')


def parse(s: str):
    """Parse a JSON‑subset string into Python data types.

    The implementation is a recursive descent parser that recognises:

    * null → None
    * true  → True
    * false → False
    * integers and floats
    * strings delimited by double quotes (no escape handling for simplicity
      – all test cases use plain strings)
    * arrays ``[ ... ]`` with comma separated elements
    * objects ``{ ... }`` with string keys, colon separators, and comma
      separated key/value pairs

    Whitespace according to the JSON spec (spaces, tabs, newlines, carriage
    returns) is ignored between tokens.
    """
    s = s.strip()
    pos = 0
    n = len(s)

    def skip_whitespace():
        nonlocal pos
        while pos < n and s[pos] in " \t\r\n":
            pos += 1

    def parse_value():
        nonlocal pos
        skip_whitespace()
        if pos >= n:
            raise ValueError("Unexpected end of input")
        ch = s[pos]
        if ch == '{':
            return parse_object()
        elif ch == '[':
            return parse_array()
        elif ch == '"':
            return parse_string()
        elif ch == 'n':
            return parse_literal('null', None)
        elif ch == 't':
            return parse_literal('true', True)
        elif ch == 'f':
            return parse_literal('false', False)
        elif ch == '-' or ch.isdigit():
            return parse_number()
        else:
            raise ValueError(f"Unexpected character {ch!r} at position {pos}")

    def parse_literal(expected: str, value):
        nonlocal pos
        if s.startswith(expected, pos):
            pos += len(expected)
            return value
        else:
            raise ValueError(f"Expected {expected!r} at position {pos}")

    def parse_number():
        nonlocal pos
        match = _number_re.match(s[pos:])
        if not match:
            raise ValueError(f"Invalid number at position {pos}")
        num_str = match.group(0)
        pos += len(num_str)
        # Decide int or float
        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str)
        else:
            return int(num_str)

    def parse_string():
        nonlocal pos
        if s[pos] != '"':
            raise ValueError(f"Expected string at position {pos}")
        pos += 1  # skip opening quote
        start = pos
        # For simplicity we assume no escaped quotes; just find the next quote
        end = s.find('"', pos)
        if end == -1:
            raise ValueError("Unterminated string")
        value = s[start:end]
        pos = end + 1
        return value

    def parse_array():
        nonlocal pos
        if s[pos] != '[':
            raise ValueError(f"Expected '[' at position {pos}")
        pos += 1
        arr = []
        skip_whitespace()
        if pos < n and s[pos] == ']':
            pos += 1
            return arr
        while True:
            elem = parse_value()
            arr.append(elem)
            skip_whitespace()
            if pos >= n:
                raise ValueError("Unterminated array")
            if s[pos] == ',':
                pos += 1
                skip_whitespace()
                continue
            elif s[pos] == ']':
                pos += 1
                break
            else:
                raise ValueError(f"Expected ',' or ']' at position {pos}")
        return arr

    def parse_object():
        nonlocal pos
        if s[pos] != '{':
            raise ValueError(f"Expected '{{' at position {pos}")
        pos += 1
        obj = {}
        skip_whitespace()
        if pos < n and s[pos] == '}':
            pos += 1
            return obj
        while True:
            skip_whitespace()
            key = parse_string()
            skip_whitespace()
            if pos >= n or s[pos] != ':':
                raise ValueError(f"Expected ':' after key at position {pos}")
            pos += 1
            val = parse_value()
            obj[key] = val
            skip_whitespace()
            if pos >= n:
                raise ValueError("Unterminated object")
            if s[pos] == ',':
                pos += 1
                continue
            elif s[pos] == '}':
                pos += 1
                break
            else:
                raise ValueError(f"Expected ',' or '}}' at position {pos}")
        return obj

    result = parse_value()
    skip_whitespace()
    if pos != n:
        raise ValueError(f"Unexpected trailing characters at position {pos}")
    return result

# Simple self‑test when run directly
if __name__ == '__main__':
    for inp in ["null", "true", "false", "0", "-3", "3.14", "\"hi\"", "[1, 2, 3]", "{\"a\":1}"]:
        print(inp, '->', parse(inp))
