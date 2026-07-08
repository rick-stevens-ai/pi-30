# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
def parse(s):
    idx = [0]  # Use list for mutable reference in nested functions
    
    def skip_whitespace():
        while idx[0] < len(s) and s[idx[0]] in ' \t\n\r':
            idx[0] += 1
    
    def parse_value():
        skip_whitespace()
        if idx[0] >= len(s):
            raise ValueError("unexpected end of input")
        
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
            raise ValueError(f"unexpected character: {c}")
    
    def parse_null():
        if s[idx[0]:idx[0]+4] == 'null':
            idx[0] += 4
            return None
        raise ValueError("expected 'null'")
    
    def parse_true():
        if s[idx[0]:idx[0]+4] == 'true':
            idx[0] += 4
            return True
        raise ValueError("expected 'true'")
    
    def parse_false():
        if s[idx[0]:idx[0]+5] == 'false':
            idx[0] += 5
            return False
        raise ValueError("expected 'false'")
    
    def parse_string():
        idx[0] += 1  # skip opening quote
        start = idx[0]
        result = []
        while idx[0] < len(s):
            c = s[idx[0]]
            if c == '"':
                result.append(s[start:idx[0]])
                idx[0] += 1  # skip closing quote
                return ''.join(result)
            elif c == '\\':
                result.append(s[start:idx[0]])
                idx[0] += 1
                if idx[0] >= len(s):
                    raise ValueError("unexpected end of string escape")
                escaped = s[idx[0]]
                if escaped == 'n':
                    result.append('\n')
                elif escaped == 't':
                    result.append('\t')
                elif escaped == 'r':
                    result.append('\r')
                elif escaped == '"':
                    result.append('"')
                elif escaped == '\\':
                    result.append('\\')
                else:
                    result.append(escaped)
                idx[0] += 1
                start = idx[0]
            else:
                idx[0] += 1
        raise ValueError("unterminated string")
    
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
            return float(s[start:idx[0]])
        return int(s[start:idx[0]])
    
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
                raise ValueError("unexpected end of array")
            if s[idx[0]] == ']':
                idx[0] += 1
                return result
            if s[idx[0]] != ',':
                raise ValueError("expected ',' in array")
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
                raise ValueError("expected ':' in object")
            idx[0] += 1
            value = parse_value()
            result[key] = value
            skip_whitespace()
            if idx[0] >= len(s):
                raise ValueError("unexpected end of object")
            if s[idx[0]] == '}':
                idx[0] += 1
                return result
            if s[idx[0]] != ',':
                raise ValueError("expected ',' in object")
            idx[0] += 1
    
    return parse_value()