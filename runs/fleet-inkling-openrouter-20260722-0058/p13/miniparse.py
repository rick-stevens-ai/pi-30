def parse(s):
    s = s.strip()
    # Use index-based parser
    class Parser:
        def __init__(self, text):
            self.text = text
            self.i = 0
            self.n = len(text)
        def skip_ws(self):
            while self.i < self.n and self.text[self.i] in ' \t\n\r':
                self.i += 1
        def peek(self):
            self.skip_ws()
            if self.i < self.n:
                return self.text[self.i]
            return None
        def parse_value(self):
            self.skip_ws()
            ch = self.text[self.i]
            if ch == 'n':
                self.i += 4
                return None
            elif ch == 't':
                self.i += 4
                return True
            elif ch == 'f':
                self.i += 5
                return False
            elif ch == '"':
                return self.parse_string()
            elif ch == '[':
                return self.parse_array()
            elif ch == '{':
                return self.parse_object()
            elif ch == '-' or ch.isdigit():
                return self.parse_number()
            else:
                raise ValueError("invalid")
        def parse_string(self):
            self.i += 1  # skip opening quote
            chars = []
            while self.i < self.n and self.text[self.i] != '"':
                chars.append(self.text[self.i])
                self.i += 1
            self.i += 1  # skip closing quote
            return ''.join(chars)
        def parse_number(self):
            start = self.i
            if self.text[self.i] == '-':
                self.i += 1
            while self.i < self.n and self.text[self.i].isdigit():
                self.i += 1
            if self.i < self.n and self.text[self.i] == '.':
                self.i += 1
                while self.i < self.n and self.text[self.i].isdigit():
                    self.i += 1
            num_str = self.text[start:self.i]
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        def parse_array(self):
            self.i += 1  # skip [
            arr = []
            while True:
                self.skip_ws()
                if self.i >= self.n or self.text[self.i] == ']':
                    self.i += 1
                    return arr
                arr.append(self.parse_value())
                self.skip_ws()
                if self.i < self.n and self.text[self.i] == ',':
                    self.i += 1
                elif self.text[self.i] == ']':
                    self.i += 1
                    return arr
                else:
                    raise ValueError("bad array")
        def parse_object(self):
            self.i += 1  # skip {
            obj = {}
            while True:
                self.skip_ws()
                if self.i >= self.n or self.text[self.i] == '}':
                    self.i += 1
                    return obj
                key = self.parse_string()
                self.skip_ws()
                if self.text[self.i] == ':':
                    self.i += 1
                else:
                    raise ValueError("bad object")
                val = self.parse_value()
                obj[key] = val
                self.skip_ws()
                if self.i < self.n and self.text[self.i] == ',':
                    self.i += 1
                elif self.text[self.i] == '}':
                    self.i += 1
                    return obj
                else:
                    raise ValueError("bad object")
    parser = Parser(s)
    return parser.parse_value()
