import re

class JSONParser:
    def __init__(self, s):
        self.s = s
        self.pos = 0

    def skip_whitespace(self):
        while self.pos < len(self.s) and self.s[self.pos].isspace():
            self.pos += 1

    def parse_value(self):
        self.skip_whitespace()
        if self.pos >= len(self.s):
            return None

        char = self.s[self.pos]

        if char == '"':
            return self.parse_string()
        elif char == '{':
            return self.parse_object()
        elif char == '[':
            return self.parse_array()
        elif char.isdigit() or char == '-':
            return self.parse_number()
        elif self.s.startswith('true', self.pos):
            self.pos += 4
            return True
        elif self.s.startswith('false', self.pos):
            self.pos += 5
            return False
        elif self.s.startswith('null', self.pos):
            self.pos += 4
            return None
        else:
            raise ValueError(f"Unexpected character at position {self.pos}: {char}")

    def parse_string(self):
        self.pos += 1  # skip opening quote
        start = self.pos
        while self.pos < len(self.s) and self.s[self.pos] != '"':
            self.pos += 1
        result = self.s[start:self.pos]
        if self.pos < len(self.s):
            self.pos += 1  # skip closing quote
        return result

    def parse_number(self):
        start = self.pos
        if self.s[self.pos] == '-':
            self.pos += 1
        
        while self.pos < len(self.s) and (self.s[self.pos].isdigit() or self.s[self.pos] == '.'):
            self.pos += 1
        
        num_str = self.s[start:self.pos]
        if '.' in num_str:
            return float(num_str)
        else:
            return int(num_str)

    def parse_array(self):
        self.pos += 1  # skip [
        self.skip_whitespace()
        arr = []
        if self.pos < len(self.s) and self.s[self.pos] == ']':
            self.pos += 1
            return arr
        
        while True:
            arr.append(self.parse_value())
            self.skip_whitespace()
            if self.pos >= len(self.s):
                break
            if self.s[self.pos] == ',':
                self.pos += 1
                self.skip_whitespace()
            elif self.s[self.pos] == ']':
                self.pos += 1
                break
            else:
                raise ValueError(f"Expected , or ] at position {self.pos}")
        return arr

    def parse_object(self):
        self.pos += 1  # skip {
        self.skip_whitespace()
        obj = {}
        if self.pos < len(self.s) and self.s[self.pos] == '}':
            self.pos += 1
            return obj
        
        while True:
            key = self.parse_string()
            self.skip_whitespace()
            if self.pos >= len(self.s) or self.s[self.pos] != ':':
                raise ValueError(f"Expected : at position {self.pos}")
            self.pos += 1
            self.skip_whitespace()
            value = self.parse_value()
            obj[key] = value
            self.skip_whitespace()
            if self.pos >= len(self.s):
                break
            if self.s[self.pos] == ',':
                self.pos += 1
                self.skip_whitespace()
            elif self.s[self.pos] == '}':
                self.pos += 1
                break
            else:
                raise ValueError(f"Expected , or }} at position {self.pos}")
        return obj

def parse(s):
    parser = JSONParser(s)
    result = parser.parse_value()
    parser.skip_whitespace()
    return result
