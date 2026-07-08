def parse( s ):
    pos = 0

    def skip_ws():
        nonlocal pos
        while pos < len(s) and s[pos].isspace():
            pos += 1

    def peek():
        return s[pos] if pos < len(s) else None

    def advance(n=1):
        nonlocal pos
        pos += n

    # ----- literals -------------------------------------------------------
    def parse_string():
        # assume current char is the opening quote
        advance(1)                     # skip quote
        content = []
        while True:
            ch = peek()
            if ch is None or ch == '"':
                # found closing quote
                advance(1)
                break
            content.append(ch)
            advance(1)
        return ''.join(content)

    def parse_number():
        start = pos
        if s[pos] == '-':
            advance(1)                 # consume minus
            if pos >= len(s):
                raise SyntaxError('Invalid number')
        num_chars = []
        dot_seen = False
        while pos < len(s):
            ch = s[pos]
            if ch.isdigit():
                num_chars.append(ch)
                advance(1)
            elif ch == '.':
                if dot_seen:               # second dot – not allowed in JSON numbers
                    break
                dot_seen = True
                num_chars.append(ch)
                advance(1)
            else:
                break

        if not num_chars:
            raise SyntaxError('Number has no digits')
        # ensure at least one digit
        if not any(c.isdigit() for c in num_chars):
            raise SyntaxError('Number contains only a sign or dot')
        num_str = ''.join(num_chars)
        try:
            return int(num_str) if '.' not in num_str else float(num_str)
        except ValueError:
            raise SyntaxError('Invalid numeric literal')

    def parse_true():
        if s.startswith('true', pos):
            advance(4)
            return True
        raise SyntaxError("Expected \"true\"")

    def parse_false():
        if s.startswith('false', pos):
            advance(5)
            return False
        raise SyntaxError("Expected \"false\"")

    def parse_null():
        if s.startswith('null', pos):
            advance(4)
            return None
        raise SyntaxError("Expected \"null\"")

    # ----- containers ------------------------------------------------------
    def parse_array():
        # expect '['
        advance(1)                     # consume '['
        skip_ws()
        if peek() == ']':
            advance(1)                 # ']'
            return []
        items = []
        while True:
            items.append(parse_value())
            skip_ws()
            ch = peek()
            if ch == ',':
                advance(1)
                skip_ws()
                continue
            elif ch == ']':
                advance(1)
                break
            else:
                raise SyntaxError('Expected \",\" or \"]\" in array')
        return items

    def parse_object():
        # expect '{'
        advance(1)                     # consume '{'
        skip_ws()
        if peek() == '}':
            advance(1)
            return {}
        obj = {}
        while True:
            # key is a quoted string
            start_quote = s.find('"', pos)
            if start_quote == -1:
                raise SyntaxError('Missing opening quote for object key')
            end_quote = s.find('"', start_quote + 1)
            if end_quote == -1:
                raise SyntaxError('Missing closing quote for object key')
            key = s[start_quote + 1:end_quote]
            pos = end_quote + 1
            skip_ws()
            # ':'
            if peek() != ':':
                raise SyntaxError('Expected ":" after object key')
            advance(1)
            skip_ws()
            val = parse_value()
            obj[key] = val
            skip_ws()
            ch = peek()
            if ch == ',':
                advance(1)
                skip_ws()
                continue
            elif ch == '}':
                advance(1)
                break
            else:
                raise SyntaxError('Expected "," or "}" in object')
        return obj

    # ----- main parser ----------------------------------------------------
    def parse_value():
        skip_ws()
        if pos >= len(s):
            raise SyntaxError('Unexpected end of input')
        ch = peek()
        if ch == '"':
            return parse_string()
        elif ch == '-' or ch.isdigit():
            return parse_number()
        elif s.startswith('true', pos):
            return parse_true()
        elif s.startswith('false', pos):
            return parse_false()
        elif s.startswith('null', pos):
            return parse_null()
        elif ch == '[':
            return parse_array()
        elif ch == '{':
            return parse_object()
        else:
            raise SyntaxError(f'Unexpected character {ch!r}')

    return parse_value()

