# P13 tiny JSON-subset parser (no eval, no json module).
# Supports null/true/false, ints, floats, strings, arrays, objects, nesting,
# and whitespace. Implements a recursive‑descent parser.

def parse(s):
    """Parse a JSON‑like string *s* and return the corresponding Python value.
    Supports a subset of JSON as required by the tests.
    """
    i = 0
    n = len(s)

    def skip_ws():
        nonlocal i
        while i < n and s[i].isspace():
            i += 1

    def parse_value():
        nonlocal i
        skip_ws()
        if i >= n:
            raise ValueError('Unexpected end of input')
        ch = s[i]
        # literals
        if s.startswith('null', i):
            i += 4
            return None
        if s.startswith('true', i):
            i += 4
            return True
        if s.startswith('false', i):
            i += 5
            return False
        if ch == '"':
            return parse_string()
        if ch == '[':
            return parse_array()
        if ch == '{':
            return parse_object()
        # number
        return parse_number()

    def parse_string():
        nonlocal i
        i += 1  # skip opening quote
        sb = []
        while i < n:
            c = s[i]
            if c == '\\':
                i += 1
                if i >= n:
                    break
                esc = s[i]
                mapping = {
                    '"': '"',
                    '\\': '\\',
                    '/': '/',
                    'b': '\b',
                    'f': '\f',
                    'n': '\n',
                    'r': '\r',
                    't': '\t',
                }
                sb.append(mapping.get(esc, esc))
                i += 1
                continue
            if c == '"':
                i += 1
                break
            sb.append(c)
            i += 1
        return ''.join(sb)

    def parse_number():
        nonlocal i
        start = i
        if s[i] in '+-':
            i += 1
        while i < n and s[i].isdigit():
            i += 1
        is_float = False
        if i < n and s[i] == '.':
            is_float = True
            i += 1
            while i < n and s[i].isdigit():
                i += 1
        num_str = s[start:i]
        return float(num_str) if is_float else int(num_str)

    def parse_array():
        nonlocal i
        i += 1  # skip '['
        arr = []
        while True:
            skip_ws()
            if i < n and s[i] == ']':
                i += 1
                break
            arr.append(parse_value())
            skip_ws()
            if i < n and s[i] == ',':
                i += 1
                continue
            if i < n and s[i] == ']':
                i += 1
                break
            raise ValueError('Expected , or ] in array')
        return arr

    def parse_object():
        nonlocal i
        i += 1  # skip '{'
        obj = {}
        while True:
            skip_ws()
            if i < n and s[i] == '}':
                i += 1
                break
            key = parse_string()
            skip_ws()
            if i >= n or s[i] != ':':
                raise ValueError('Expected : after object key')
            i += 1
            value = parse_value()
            obj[key] = value
            skip_ws()
            if i < n and s[i] == ',':
                i += 1
                continue
            if i < n and s[i] == '}':
                i += 1
                break
            raise ValueError('Expected , or } in object')
        return obj

    result = parse_value()
    skip_ws()
    if i != n:
        raise ValueError('Extra data after parsing')
    return result

