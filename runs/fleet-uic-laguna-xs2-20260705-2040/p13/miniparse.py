# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
class Parser:
    def __init__(self, s):
        self.s = s
        self.pos = 0
    
    def skip_ws(self):
        while self.pos < len(self.s) and self.s[self.pos] in ' \t\n\r':
            self.pos += 1
    
    def peek(self):
        self.skip_ws()
        if self.pos >= len(self.s):
            return None
        return self.s[self.pos]
    
    def advance(self):
        self.skip_ws()
        if self.pos >= len(self.s):
            raise ValueError("unexpected end")
        ch = self.s[self.pos]
        self.pos += 1
        return ch
    
    def parse_value(self):
        ch = self.peek()
        if ch is None:
            raise ValueError("unexpected end")
        if ch == 'n':
            return self.parse_null()
        elif ch == 't':
            return self.parse_true()
        elif ch == 'f':
            return self.parse_false()
        elif ch == '"':
            return self.parse_string()
        elif ch == '[':
            return self.parse_array()
        elif ch == '{':
            return self.parse_object()
        elif ch == '-' or ch.isdigit():
            return self.parse_number()
        else:
            raise ValueError(f"unexpected character: {ch}")
    
    def parse_null(self):
        if self.s[self.pos:self.pos+4] != 'null':
            raise ValueError("expected null")
        self.pos += 4
        return None
    
    def parse_true(self):
        if self.s[self.pos:self.pos+4] != 'true':
            raise ValueError("expected true")
        self.pos += 4
        return True
    
    def parse_false(self):
        if self.s[self.pos:self.pos+5] != 'false':
            raise ValueError("expected false")
        self.pos += 5
        return False
    
    def parse_string(self):
        self.advance()  # consume opening "
        result = []
        while self.pos < len(self.s):
            ch = self.s[self.pos]
            if ch == '"':
                self.pos += 1
                return ''.join(result)
            elif ch == '\\':
                self.pos += 1
                if self.pos >= len(self.s):
                    raise ValueError("unexpected end in escape")
                esc = self.s[self.pos]
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
                self.pos += 1
            else:
                result.append(ch)
                self.pos += 1
        raise ValueError("unterminated string")
    
    def parse_number(self):
        start = self.pos
        if self.s[self.pos] == '-':
            self.pos += 1
        while self.pos < len(self.s) and self.s[self.pos].isdigit():
            self.pos += 1
        if self.pos < len(self.s) and self.s[self.pos] == '.':
            self.pos += 1
            while self.pos < len(self.s) and self.s[self.pos].isdigit():
                self.pos += 1
        num_str = self.s[start:self.pos]
        if '.' in num_str:
            return float(num_str)
        return int(num_str)
    
    def parse_array(self):
        self.advance()  # consume [
        result = []
        if self.peek() == ']':
            self.advance()
            return result
        while True:
            result.append(self.parse_value())
            if self.peek() == ']':
                self.advance()
                return result
            if self.advance() != ',':
                raise ValueError("expected , in array")
    
    def parse_object(self):
        self.advance()  # consume {
        result = {}
        if self.peek() == '}':
            self.advance()
            return result
        while True:
            key = self.parse_string()
            if self.advance() != ':':
                raise ValueError("expected : in object")
            value = self.parse_value()
            result[key] = value
            if self.peek() == '}':
                self.advance()
                return result
            if self.advance() != ',':
                raise ValueError("expected , in object")

def parse(s):
    p = Parser(s)
    return p.parse_value()