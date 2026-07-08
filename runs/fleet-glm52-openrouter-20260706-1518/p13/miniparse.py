# P13: a tiny JSON-subset parser (no eval, no json module).
# Supports null/true/false, ints, floats, strings, arrays, objects, nesting,
# whitespace.


def parse(s):
    pos = [0]
    n = len(s)

    def skip_ws():
        while pos[0] < n and s[pos[0]] in " \t\n\r":
            pos[0] += 1

    def parse_value():
        skip_ws()
        if pos[0] >= n:
            raise ValueError("unexpected end")
        c = s[pos[0]]
        if c == '{':
            return parse_object()
        if c == '[':
            return parse_array()
        if c == '"':
            return parse_string()
        if c == 't':
            return parse_true()
        if c == 'f':
            return parse_false()
        if c == 'n':
            return parse_null()
        return parse_number()

    def parse_true():
        if s[pos[0]:pos[0] + 4] == "true":
            pos[0] += 4
            return True
        raise ValueError("expected true")

    def parse_false():
        if s[pos[0]:pos[0] + 5] == "false":
            pos[0] += 5
            return False
        raise ValueError("expected false")

    def parse_null():
        if s[pos[0]:pos[0] + 4] == "null":
            pos[0] += 4
            return None
        raise ValueError("expected null")

    def parse_number():
        start = pos[0]
        if pos[0] < n and s[pos[0]] in "+-":
            pos[0] += 1
        while pos[0] < n and s[pos[0]].isdigit():
            pos[0] += 1
        is_float = False
        if pos[0] < n and s[pos[0]] == '.':
            is_float = True
            pos[0] += 1
            while pos[0] < n and s[pos[0]].isdigit():
                pos[0] += 1
        if pos[0] < n and s[pos[0]] in "eE":
            is_float = True
            pos[0] += 1
            if pos[0] < n and s[pos[0]] in "+-":
                pos[0] += 1
            while pos[0] < n and s[pos[0]].isdigit():
                pos[0] += 1
        text = s[start:pos[0]]
        if text == "":
            raise ValueError("invalid number")
        return float(text) if is_float else int(text)

    def parse_string():
        pos[0] += 1  # skip opening quote
        result = []
        while pos[0] < n:
            c = s[pos[0]]
            if c == '"':
                pos[0] += 1
                return "".join(result)
            if c == '\\':
                pos[0] += 1
                if pos[0] >= n:
                    raise ValueError("unterminated escape")
                e = s[pos[0]]
                if e == '"':
                    result.append('"')
                elif e == '\\':
                    result.append('\\')
                elif e == '/':
                    result.append('/')
                elif e == 'b':
                    result.append('\b')
                elif e == 'f':
                    result.append('\f')
                elif e == 'n':
                    result.append('\n')
                elif e == 'r':
                    result.append('\r')
                elif e == 't':
                    result.append('\t')
                elif e == 'u':
                    hexdigits = s[pos[0] + 1:pos[0] + 5]
                    if len(hexdigits) < 4:
                        raise ValueError("bad unicode escape")
                    result.append(chr(int(hexdigits, 16)))
                    pos[0] += 4
                else:
                    raise ValueError("bad escape: " + e)
                pos[0] += 1
            else:
                result.append(c)
                pos[0] += 1
        raise ValueError("unterminated string")

    def parse_array():
        pos[0] += 1  # skip [
        arr = []
        skip_ws()
        if pos[0] < n and s[pos[0]] == ']':
            pos[0] += 1
            return arr
        while True:
            arr.append(parse_value())
            skip_ws()
            if pos[0] >= n:
                raise ValueError("unterminated array")
            c = s[pos[0]]
            if c == ',':
                pos[0] += 1
                continue
            if c == ']':
                pos[0] += 1
                return arr
            raise ValueError("expected , or ]")

    def parse_object():
        pos[0] += 1  # skip {
        obj = {}
        skip_ws()
        if pos[0] < n and s[pos[0]] == '}':
            pos[0] += 1
            return obj
        while True:
            skip_ws()
            if pos[0] >= n or s[pos[0]] != '"':
                raise ValueError("expected key string")
            key = parse_string()
            skip_ws()
            if pos[0] >= n or s[pos[0]] != ':':
                raise ValueError("expected :")
            pos[0] += 1
            obj[key] = parse_value()
            skip_ws()
            if pos[0] >= n:
                raise ValueError("unterminated object")
            c = s[pos[0]]
            if c == ',':
                pos[0] += 1
                continue
            if c == '}':
                pos[0] += 1
                return obj
            raise ValueError("expected , or }")

    result = parse_value()
    skip_ws()
    if pos[0] != n:
        raise ValueError("trailing characters")
    return result
