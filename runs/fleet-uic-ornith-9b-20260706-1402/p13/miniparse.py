# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
def parse(s):
    s = s.strip()
    if not s:
        raise ValueError("empty input")
    pos = [0]

    def peek():
        return s[pos[0]]

    def advance():
        ch = s[pos[0]]
        pos[0] += 1
        return ch

    def skip_ws():
        while pos[0] < len(s) and s[pos[0]].isspace():
            pos[0] += 1

    def parse_value():
        skip_ws()
        if peek() == 'n':
            return parse_null()
        elif peek() == 't':
            return parse_true()
        elif peek() == 'f':
            return parse_false()
        elif peek() in ('"', "[", "{"):
            return parse_quoted_or_container()
        else:
            return parse_number()

    def parse_null():
        assert s[pos[0]:pos[0]+4] == "null"
        pos[0] += 4
        skip_ws()
        return None

    def parse_true():
        assert s[pos[0]:pos[0]+4] == "true"
        pos[0] += 4
        skip_ws()
        return True

    def parse_false():
        assert s[pos[0]:pos[0]+5] == "false"
        pos[0] += 5
        skip_ws()
        return False

    def parse_quoted_or_container():
        if peek() == '"':
            return parse_string()
        elif peek() == '[':
            return parse_array()
        elif peek() == '{':
            return parse_object()
        else:
            raise ValueError(f"unexpected character {peek!r}")

    def parse_string():
        assert peek() == '"'
        pos[0] += 1  # skip opening quote
        result = []
        while pos[0] < len(s) and s[pos[0]] != '"':
            ch = s[pos[0]]
            if ch == '\\':
                pos[0] += 1
                esc = s[pos[0]]
                if esc == '"':
                    result.append('"')
                elif esc == '\\':
                    result.append('\\')
                elif esc == '/':
                    result.append('/')
                elif esc == 'b':
                    result.append('\b')
                elif esc == 'f':
                    result.append('\f')
                elif esc == 'n':
                    result.append('\n')
                elif esc == 'r':
                    result.append('\r')
                elif esc == 't':
                    result.append('\t')
                elif esc == 'u':
                    # 4 hex digits
                    h = s[pos[0]+1:pos[0]+5]
                    result.append(chr(int(h, 16)))
                    pos[0] += 4
            else:
                result.append(ch)
            pos[0] += 1
        assert pos[0] < len(s), "unterminated string"
        pos[0] += 1  # skip closing quote
        return ''.join(result)

    def parse_number():
        start = pos[0]
        if peek() == '-':
            pos[0] += 1
        while pos[0] < len(s) and s[pos[0]].isdigit():
            pos[0] += 1
        is_float = False
        if pos[0] < len(s) and s[pos[0]] == '.':
            is_float = True
            pos[0] += 1
            while pos[0] < len(s) and s[pos[0]].isdigit():
                pos[0] += 1
        # Exponent
        if pos[0] < len(s) and s[pos[0]] in ('e', 'E'):
            is_float = True
            pos[0] += 1
            if pos[0] < len(s) and s[pos[0]] in ('+', '-'):
                pos[0] += 1
            while pos[0] < len(s) and s[pos[0]].isdigit():
                pos[0] += 1
        text = s[start:pos[0]]
        skip_ws()
        if is_float or '.' in text or 'e' in text.lower():
            return float(text)
        else:
            return int(text)

    def parse_array():
        assert peek() == '['
        pos[0] += 1
        result = []
        skip_ws()
        if peek() == ']':
            pos[0] += 1
            skip_ws()
            return result
        while True:
            val = parse_value()
            result.append(val)
            skip_ws()
            ch = peek()
            if ch == ',':
                pos[0] += 1
                skip_ws()
                continue
            elif ch == ']':
                pos[0] += 1
                skip_ws()
                return result
            else:
                raise ValueError(f"expected ',' or ']' got {ch!r}")

    def parse_object():
        assert peek() == '{'
        pos[0] += 1
        result = {}
        skip_ws()
        if peek() == '}':
            pos[0] += 1
            skip_ws()
            return result
        while True:
            skip_ws()
            key_str = parse_string()
            skip_ws()
            assert s[pos[0]] == ':', f"expected ':' got {s[pos[0]]!r}"
            pos[0] += 1
            val = parse_value()
            result[key_str] = val
            skip_ws()
            ch = peek()
            if ch == ',':
                pos[0] += 1
                skip_ws()
                continue
            elif ch == '}':
                pos[0] += 1
                skip_ws()
                return result
            else:
                raise ValueError(f"expected ',' or '}}' got {ch!r}")

    val = parse_value()
    skip_ws()
    if pos[0] != len(s):
        remaining = s[pos[0]:].strip()
        raise ValueError(f"unexpected trailing content: {remaining!r}")
    return val
