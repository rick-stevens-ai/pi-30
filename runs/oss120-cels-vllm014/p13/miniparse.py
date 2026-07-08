# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
# Updated to parse a JSON subset: null, true, false, numbers (int/float), strings, arrays, objects,
# with proper handling of whitespace and nesting.

def parse(s):
    """Parse a JSON-like string into Python data structures.

    Supports the following JSON subset:
        - null -> None
        - true / false -> True / False
        - numbers (integers and floating point, optional leading minus)
        - double‑quoted strings (basic escape handling for \" and \\\\)
        - arrays [] with comma‑separated values
        - objects {} with string keys and colon‑separated values
    Whitespace is ignored where permitted.
    """
    parser = _Parser(s)
    value = parser.parse_value()
    parser.skip_whitespace()
    if not parser.at_end():
        raise ValueError("Unexpected trailing characters")
    return value


class _Parser:
    def __init__(self, text: str):
        self.text = text
        self.idx = 0
        self.len = len(text)

    # Utility helpers -----------------------------------------------------
    def at_end(self):
        return self.idx >= self.len

    def peek(self):
        return self.text[self.idx] if not self.at_end() else ''

    def consume(self, expected: str = None):
        if self.at_end():
            raise ValueError("Unexpected end of input")
        ch = self.text[self.idx]
        if expected is not None and ch != expected:
            raise ValueError(f"Expected '{expected}' but got '{ch}' at position {self.idx}")
        self.idx += 1
        return ch

    def skip_whitespace(self):
        while not self.at_end() and self.peek() in ' \t\n\r':
            self.idx += 1

    # Parsing entry point -------------------------------------------------
    def parse_value(self):
        self.skip_whitespace()
        if self.at_end():
            raise ValueError("Empty input")
        ch = self.peek()
        if ch == 'n':
            return self.parse_null()
        if ch == 't':
            return self.parse_true()
        if ch == 'f':
            return self.parse_false()
        if ch == '"':
            return self.parse_string()
        if ch == '[':
            return self.parse_array()
        if ch == '{':
            return self.parse_object()
        if ch == '-' or ch.isdigit():
            return self.parse_number()
        raise ValueError(f"Unexpected character '{ch}' at position {self.idx}")

    # Literal parsers ------------------------------------------------------
    def parse_null(self):
        if self.text[self.idx:self.idx+4] != 'null':
            raise ValueError("Invalid literal, expected 'null'")
        self.idx += 4
        return None

    def parse_true(self):
        if self.text[self.idx:self.idx+4] != 'true':
            raise ValueError("Invalid literal, expected 'true'")
        self.idx += 4
        return True

    def parse_false(self):
        if self.text[self.idx:self.idx+5] != 'false':
            raise ValueError("Invalid literal, expected 'false'")
        self.idx += 5
        return False

    # Number parser --------------------------------------------------------
    def parse_number(self):
        start = self.idx
        # optional minus
        if self.peek() == '-':
            self.idx += 1
        # integer part
        if self.at_end():
            raise ValueError("Invalid number")
        if self.peek() == '0':
            self.idx += 1
        elif self.peek().isdigit():
            while not self.at_end() and self.peek().isdigit():
                self.idx += 1
        else:
            raise ValueError("Invalid number")
        # fractional part
        if not self.at_end() and self.peek() == '.':
            self.idx += 1
            if self.at_end() or not self.peek().isdigit():
                raise ValueError("Invalid fractional part in number")
            while not self.at_end() and self.peek().isdigit():
                self.idx += 1
            is_float = True
        else:
            is_float = False
        # exponent part (optional, simple support)
        if not self.at_end() and self.peek() in 'eE':
            self.idx += 1
            if not self.at_end() and self.peek() in '+-':
                self.idx += 1
            if self.at_end() or not self.peek().isdigit():
                raise ValueError("Invalid exponent in number")
            while not self.at_end() and self.peek().isdigit():
                self.idx += 1
            is_float = True
        num_str = self.text[start:self.idx]
        try:
            return float(num_str) if is_float else int(num_str)
        except ValueError as exc:
            raise ValueError(f"Invalid number '{num_str}'") from exc

    # String parser --------------------------------------------------------
    def parse_string(self):
        if self.consume('"') is None:
            pass  # consume will raise if not a quote
        result_chars = []
        while not self.at_end():
            ch = self.consume()
            if ch == '"':
                return ''.join(result_chars)
            if ch == '\\':
                if self.at_end():
                    raise ValueError("Invalid escape at end of string")
                esc = self.consume()
                if esc == '"':
                    result_chars.append('"')
                elif esc == '\\':
                    result_chars.append('\\')
                elif esc == '/':
                    result_chars.append('/')
                elif esc == 'b':
                    result_chars.append('\b')
                elif esc == 'f':
                    result_chars.append('\f')
                elif esc == 'n':
                    result_chars.append('\n')
                elif esc == 'r':
                    result_chars.append('\r')
                elif esc == 't':
                    result_chars.append('\t')
                else:
                    # For simplicity, unsupported escapes are treated as literal
                    result_chars.append('\\' + esc)
                continue
            result_chars.append(ch)
        raise ValueError("Unterminated string literal")

    # Array parser ----------------------------------------------------------
    def parse_array(self):
        self.consume('[')
        arr = []
        self.skip_whitespace()
        if not self.at_end() and self.peek() == ']':
            self.consume(']')
            return arr
        while True:
            arr.append(self.parse_value())
            self.skip_whitespace()
            if self.at_end():
                raise ValueError("Unterminated array")
            if self.peek() == ',':
                self.consume(',')
                self.skip_whitespace()
                continue
            if self.peek() == ']':
                self.consume(']')
                return arr
            raise ValueError(f"Expected ',' or ']' in array at position {self.idx}")

    # Object parser ---------------------------------------------------------
    def parse_object(self):
        self.consume('{')
        obj = {}
        self.skip_whitespace()
        if not self.at_end() and self.peek() == '}':
            self.consume('}')
            return obj
        while True:
            self.skip_whitespace()
            if self.peek() != '"':
                raise ValueError(f"Object keys must be strings at position {self.idx}")
            key = self.parse_string()
            self.skip_whitespace()
            self.consume(':')
            self.skip_whitespace()
            value = self.parse_value()
            obj[key] = value
            self.skip_whitespace()
            if self.at_end():
                raise ValueError("Unterminated object")
            if self.peek() == ',':
                self.consume(',')
                continue
            if self.peek() == '}':
                self.consume('}')
                return obj
            raise ValueError(f"Expected ',' or '}}' in object at position {self.idx}")

