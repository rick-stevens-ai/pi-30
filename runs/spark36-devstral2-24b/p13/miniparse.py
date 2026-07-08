# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
def parse(s):
    pos = 0
    
    def skip_whitespace():
        nonlocal pos
        while pos < len(s) and s[pos] in ' \t\n\r':
            pos += 1
    
    result = None

    
    def parse_value():
        nonlocal pos, result
        skip_whitespace()
        if pos >= len(s):
            raise ValueError("Unexpected end of input")
        
        c = s[pos]
        if c == 'n' and s.startswith('null', pos):
            pos += 4
            result = None
            return "none"
        elif c == 't' and s.startswith('true', pos):
            pos += 4
            result = True
            return "true"
        elif c == 'f' and s.startswith('false', pos):
            pos += 5
            result = False
            return "false"
        elif c == '[':
            return parse_array()
        elif c == '{':
            return parse_object()
        elif c in '-0123456789':
            return parse_number()
        elif c == '"':
            return parse_string()
        else:
            raise ValueError(f"Unexpected character: {c}")
    
    def parse_array():
        nonlocal pos, result
        start_pos = pos
        pos += 1  # skip '['
        arr = []
        skip_whitespace()
        if s[pos] == ']':
            pos += 1
            result = arr
            return "array"
        while True:
            parse_value()  # This will set result to the parsed value
            arr.append(result)
            skip_whitespace()
            if s[pos] == ']':
                pos += 1
                result = arr
                return "array"
            elif s[pos] == ',':
                pos += 1
                continue
            else:
                raise ValueError("Expected ',' or ']' in array")
    
    def parse_object():
        nonlocal pos, result
        start_pos = pos
        pos += 1  # skip '{'
        obj = {}
        skip_whitespace()
        if s[pos] == '}':
            pos += 1
            result = obj
            return "object"
        while True:
            # Handle null as a value, not a key
            val_type = None
            key = result
            skip_whitespace()
            if s[pos] != ':':
                raise ValueError("Expected ':' in object")
            pos += 1
            parse_value()  # This will set result to the parsed value
            obj[key] = result
            skip_whitespace()
            if s[pos] == '}':
                pos += 1
                result = obj
                return "object"
            elif s[pos] == ',':
                pos += 1
                continue
            else:
                raise ValueError("Expected ',' or '}' in object")
    
    def parse_number():
        nonlocal pos, result
        start = pos
        if s[pos] == '-':
            pos += 1
        while pos < len(s) and s[pos].isdigit():
            pos += 1
        has_decimal = False
        if pos < len(s) and s[pos] == '.':
            has_decimal = True
            pos += 1
            while pos < len(s) and s[pos].isdigit():
                pos += 1
        num_str = s[start:pos]
        if '.' in num_str:
            result = float(num_str)
        else:
            result = int(num_str)
        return "number"
    
    def parse_string():
        nonlocal pos, result
        if s[pos] != '"':
            raise ValueError("Expected string to start with quotation mark")
        pos += 1
        result_str = []
        while pos < len(s) and s[pos] != '"':
            c = s[pos]
            if c == '\\':
                pos += 1
                if pos >= len(s):
                    raise ValueError("Unterminated escape sequence in string")
                result_str.append(s[pos])
            else:
                result_str.append(c)
            pos += 1
        if pos >= len(s) or s[pos] != '"':
            raise ValueError("Unterminated string")
        pos += 1
        result = ''.join(result_str)
    
    parse_value()
    skip_whitespace()
    if pos != len(s):
        raise ValueError(f"Unexpected characters at end of input: {s[pos:]}")
    return result