# P13: tiny JSON subset parser
# Supports null/true/false, integers, floats, strings, arrays, objects with nesting and whitespace.
# Implementation uses recursive descent without eval or json modules.

class _Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.len = len(s)

    def _skip_ws(self):
        while self.i < self.len and self.s[self.i] in " \t\r\n":
            self.i += 1

    def _peek(self):
        return self.s[self.i] if self.i < self.len else None

    def _consume(self, ch=None):
        if self.i >= self.len:
            raise ValueError("Unexpected end of input")
        current = self.s[self.i]
        if ch is not None and current != ch:
            raise ValueError(f"Expected '{ch}' but got '{current}' at position {self.i}")
        self.i += 1
        return current

    def _parse_value(self):
        self._skip_ws()
        ch = self._peek()
        if ch is None:
            raise ValueError("Unexpected end of input while parsing value")
        if ch == 'n':
            return self._parse_null()
        elif ch == 't':
            return self._parse_true()
        elif ch == 'f':
            return self._parse_false()
        elif ch == '"':
            return self._parse_string()
        elif ch in '-0123456789':
            return self._parse_number()
        elif ch == '[':
            return self._parse_array()
        elif ch == '{':
            return self._parse_object()
        else:
            raise ValueError(f"Unexpected character '{ch}' at position {self.i}")

    def _parse_null(self):
        expected = 'null'
        if self.s[self.i:self.i+4] != expected:
            raise ValueError("Invalid literal for null")
        self.i += 4
        return None

    def _parse_true(self):
        expected = 'true'
        if self.s[self.i:self.i+4] != expected:
            raise ValueError("Invalid literal for true")
        self.i += 4
        return True

    def _parse_false(self):
        expected = 'false'
        if self.s[self.i:self.i+5] != expected:
            raise ValueError("Invalid literal for false")
        self.i += 5
        return False

    def _parse_string(self):
        # assume starting at opening quote
        self._consume('"')
        chars = []
        while True:
            if self.i >= self.len:
                raise ValueError("Unterminated string literal")
            ch = self.s[self.i]
            if ch == '"':
                self.i += 1
                break
            elif ch == '\\':  # minimal escape support for double quote and backslash
                self.i += 1
                if self.i >= self.len:
                    raise ValueError("Unterminated escape sequence in string literal")
                esc = self.s[self.i]
                if esc == '"' or esc == '\\':
                    chars.append(esc)
                else:
                    # For simplicity, treat other escapes literally
                    chars.append('\\' + esc)
                self.i += 1
            else:
                chars.append(ch)
                self.i += 1
        return ''.join(chars)

    def _parse_number(self):
        start = self.i
        if self.s[self.i] == '-':
            self.i += 1
        has_digit = False
        while self.i < self.len and self.s[self.i].isdigit():
            self.i += 1
            has_digit = True
        if not has_digit:
            raise ValueError("Invalid number literal")
        # Fractional part
        if self.i < self.len and self.s[self.i] == '.':
            self.i += 1
            frac_has_digit = False
            while self.i < self.len and self.s[self.i].isdigit():
                self.i += 1
                frac_has_digit = True
            if not frac_has_digit:
                raise ValueError("Invalid number literal")
        # Exponent part (optional) for completeness
        if self.i < self.len and self.s[self.i] in 'eE':
            self.i += 1
            if self.i < self.len and self.s[self.i] in '+-':
                self.i += 1
            exp_has_digit = False
            while self.i < self.len and self.s[self.i].isdigit():
                self.i += 1
                exp_has_digit = True
            if not exp_has_digit:
                raise ValueError("Invalid number literal")
        num_str = self.s[start:self.i]
        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError as e:
            raise ValueError("Invalid number literal") from e

    def _parse_array(self):
        self._consume('[')
        arr = []
        while True:
            self._skip_ws()
            if self._peek() == ']':
                self._consume(']')
                break
            value = self._parse_value()
            arr.append(value)
            self._skip_ws()
            ch = self._peek()
            if ch == ',':
                self._consume(',')
                continue
            elif ch == ']':
                self._consume(']')
                break
            else:
                raise ValueError(f"Expected ',' or ']' but got '{ch}' at position {self.i}")
        return arr

    def _parse_object(self):
        self._consume('{')
        obj = {}
        while True:
            self._skip_ws()
            if self._peek() == '}':
                self._consume('}')
                break
            key = self._parse_string()
            self._skip_ws()
            self._consume(':')
            self._skip_ws()
            value = self._parse_value()
            obj[key] = value
            self._skip_ws()
            ch = self._peek()
            if ch == ',':
                self._consume(',')
                continue
            elif ch == '}':
                self._consume('}')
                break
            else:
                raise ValueError(f"Expected ',' or '}}' but got '{ch}' at position {self.i}")
        return obj

def parse(s):
    """Parse a JSON subset string into corresponding Python objects."""
    parser = _Parser(s)
    result = parser._parse_value()
    parser._skip_ws()
    if parser.i != parser.len:
        raise ValueError("Trailing characters after JSON value")
    return result

