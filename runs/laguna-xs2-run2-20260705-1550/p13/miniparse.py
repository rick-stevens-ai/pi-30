# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
def parse(s):
    idx = [0]  # Use list to allow mutation in nested functions
    
    def skip_whitespace():
        while idx[0] < len(s) and s[idx[0]] in ' \t\n\r':
            idx[0] += 1
    
    def parse_value():
        skip_whitespace()
        if idx[0] >= len(s):
            raise ValueError("Unexpected end of input")
        
        c = s[idx[0]]
        
        if c == 'n':
            return parse_null()
        elif c == 't':
            return parse_true()
        elif c == 'f':
            return parse_false()
        elif c == '"':
            return parse_string()
        elif c == '[':
            return parse_array()
        elif c == '{':
            return parse_object()
        elif c == '-' or c.isdigit():
            return parse_number()
        else:
            raise ValueError(f"Unexpected character: {c}")
    
    def parse_null():
        if s[idx[0]:idx[0]+4] != 'null':
            raise ValueError("Expected 'null'")
        idx[0] += 4
        return None
    
    def parse_true():
        if s[idx[0]:idx[0]+4] != 'true':
            raise ValueError("Expected 'true'")
        idx[0] += 4
        return True
    
    def parse_false():
        if s[idx[0]:idx[0]+5] != 'false':
            raise ValueError("Expected 'false'")
        idx[0] += 5
        return False
    
    def parse_string():
        idx[0] += 1  # skip opening quote
        start = idx[0]
        result = []
        while idx[0] < len(s):
            c = s[idx[0]]
            if c == '"':
                result.append(s[start:idx[0]])
                idx[0] += 1
                return ''.join(result)
            elif c == '\\':
                result.append(s[start:idx[0]])
                idx[0] += 1
                if idx[0] >= len(s):
                    raise ValueError("Unexpected end in escape sequence")
                esc = s[idx[0]]
                if esc == 'n':
                    result.append('\n')
                elif esc == 't':
                    result.append('\t')
                elif esc == 'r':
                    result.append('\r')
                elif esc == '"':
                    result.append('"')
                elif esc == '\\':
                    result.append('\\')
                else:
                    result.append(esc)
                idx[0] += 1
                start = idx[0]
            else:
                idx[0] += 1
        raise ValueError("Unterminated string")
    
    def parse_number():
        start = idx[0]
        if s[idx[0]] == '-':
            idx[0] += 1
        while idx[0] < len(s) and s[idx[0]].isdigit():
            idx[0] += 1
        if idx[0] < len(s) and s[idx[0]] == '.':
            idx[0] += 1
            while idx[0] < len(s) and s[idx[0]].isdigit():
                idx[0] += 1
        num_str = s[start:idx[0]]
        if '.' in num_str:
            return float(num_str)
        return int(num_str)
    
    def parse_array():
        idx[0] += 1  # skip '['
        skip_whitespace()
        if idx[0] < len(s) and s[idx[0]] == ']':
            idx[0] += 1
            return []
        result = []
        while True:
            result.append(parse_value())
            skip_whitespace()
            if idx[0] >= len(s):
                raise ValueError("Unexpected end in array")
            if s[idx[0]] == ']':
                idx[0] += 1
                return result
            if s[idx[0]] != ',':
                raise ValueError(f"Expected ',' or ']', got {s[idx[0]]}")
            idx[0] += 1
    
    def parse_object():
        idx[0] += 1  # skip '{'
        skip_whitespace()
        if idx[0] < len(s) and s[idx[0]] == '}':
            idx[0] += 1
            return {}
        result = {}
        while True:
            skip_whitespace()
            key = parse_string()
            skip_whitespace()
            if idx[0] >= len(s) or s[idx[0]] != ':':
                raise ValueError("Expected ':'")
            idx[0] += 1
            value = parse_value()
            result[key] = value
            skip_whitespace()
            if idx[0] >= len(s):
                raise ValueError("Unexpected end in object")
            if s[idx[0]] == '}':
                idx[0] += 1
                return result
            if s[idx[0]] != ',':
                raise ValueError(f"Expected ',' or '}}', got {s[idx[0]]}")
            idx[0] += 1
    
    return parse_value()