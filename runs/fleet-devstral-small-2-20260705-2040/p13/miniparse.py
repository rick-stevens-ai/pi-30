def parse(s):
    """Parse a JSON subset (null/true/false/int/float/string/array/object, nesting, whitespace)"""
    s = s.strip()
    
    def skip_whitespace(s, idx):
        while idx < len(s) and s[idx] in ' \t\n\r':
            idx += 1
        return idx
    
    def parse_value(s, idx):
        idx = skip_whitespace(s, idx)
        if idx >= len(s):
            raise ValueError("Unexpected end of input")
        
        char = s[idx]
        if char == '{':
            return parse_object(s, idx)
        elif char == '[':
            return parse_array(s, idx)
        elif char == '"':
            return parse_string(s, idx)
        elif char in '-0123456789':
            return parse_number(s, idx)
        elif s.startswith('true', idx):
            return True, idx + 4
        elif s.startswith('false', idx):
            return False, idx + 5
        elif s.startswith('null', idx):
            return None, idx + 4
        else:
            raise ValueError(f"Unexpected character: {char}")
    
    def parse_object(s, idx):
        idx += 1  # Skip '{'
        idx = skip_whitespace(s, idx)
        result = {}
        
        if idx < len(s) and s[idx] == '}':
            return result, idx + 1
        
        while True:
            idx = skip_whitespace(s, idx)
            key, idx = parse_string(s, idx)
            idx = skip_whitespace(s, idx)
            
            if idx >= len(s) or s[idx] != ':':
                raise ValueError("Expected ':' after object key")
            idx += 1
            
            value, idx = parse_value(s, idx)
            result[key] = value
            
            idx = skip_whitespace(s, idx)
            if idx >= len(s):
                raise ValueError("Unexpected end of input in object")
            
            if s[idx] == '}':
                return result, idx + 1
            elif s[idx] == ',':
                idx += 1
            else:
                raise ValueError("Expected ',' or '}' in object")
    
    def parse_array(s, idx):
        idx += 1  # Skip '['
        idx = skip_whitespace(s, idx)
        result = []
        
        if idx < len(s) and s[idx] == ']':
            return result, idx + 1
        
        while True:
            value, idx = parse_value(s, idx)
            result.append(value)
            
            idx = skip_whitespace(s, idx)
            if idx >= len(s):
                raise ValueError("Unexpected end of input in array")
            
            if s[idx] == ']':
                return result, idx + 1
            elif s[idx] == ',':
                idx += 1
            else:
                raise ValueError("Expected ',' or ']' in array")
    
    def parse_string(s, idx):
        idx += 1  # Skip '"'
        result = []
        
        while idx < len(s):
            char = s[idx]
            if char == '"':
                return ''.join(result), idx + 1
            elif char == '\\':
                idx += 1
                if idx >= len(s):
                    raise ValueError("Unexpected end of input in string")
                escape = s[idx]
                if escape == '"':
                    result.append('"')
                elif escape == '\\':
                    result.append('\\')
                elif escape == '/':
                    result.append('/')
                elif escape == 'b':
                    result.append('\b')
                elif escape == 'f':
                    result.append('\f')
                elif escape == 'n':
                    result.append('\n')
                elif escape == 'r':
                    result.append('\r')
                elif escape == 't':
                    result.append('\t')
                elif escape == 'u':
                    # Simple unicode escape - just take 4 hex digits
                    if idx + 4 >= len(s):
                        raise ValueError("Invalid unicode escape")
                    unicode_str = s[idx+1:idx+5]
                    try:
                        char_code = int(unicode_str, 16)
                        result.append(chr(char_code))
                    except ValueError:
                        raise ValueError("Invalid unicode escape")
                    idx += 4
                else:
                    raise ValueError(f"Invalid escape sequence: \\{escape}")
            else:
                result.append(char)
            idx += 1
        
        raise ValueError("Unexpected end of input in string")
    
    def parse_number(s, idx):
        start = idx
        if s[idx] == '-':
            idx += 1
        
        # Integer part
        while idx < len(s) and s[idx].isdigit():
            idx += 1
        
        # Fractional part
        if idx < len(s) and s[idx] == '.':
            idx += 1
            while idx < len(s) and s[idx].isdigit():
                idx += 1
            
            # Exponent part
            if idx < len(s) and s[idx] in 'eE':
                idx += 1
                if idx < len(s) and s[idx] in '+-':
                    idx += 1
                while idx < len(s) and s[idx].isdigit():
                    idx += 1
                
                try:
                    return float(s[start:idx]), idx
                except ValueError:
                    raise ValueError("Invalid number format")
            else:
                try:
                    return float(s[start:idx]), idx
                except ValueError:
                    raise ValueError("Invalid number format")
        
        # Exponent part for integers
        if idx < len(s) and s[idx] in 'eE':
            idx += 1
            if idx < len(s) and s[idx] in '+-':
                idx += 1
            while idx < len(s) and s[idx].isdigit():
                idx += 1
            
            try:
                return float(s[start:idx]), idx
            except ValueError:
                raise ValueError("Invalid number format")
        
        try:
            return int(s[start:idx]), idx
        except ValueError:
            raise ValueError("Invalid number format")
    
    result, idx = parse_value(s, 0)
    idx = skip_whitespace(s, idx)
    if idx != len(s):
        raise ValueError(f"Unexpected trailing characters: {s[idx:]}")
    return result
