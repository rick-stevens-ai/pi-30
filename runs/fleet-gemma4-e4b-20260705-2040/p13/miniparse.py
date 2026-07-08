# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).

class Parser:
    def __init__(self, s):
        self.s = s
        self.pos = 0

    def skip_whitespace(self):
        while self.pos < len(self.s) and self.s[self.pos] in (' ', '\t', '\n', '\r'):
            self.pos += 1

    def peek(self):
        return self.s[self.pos] if self.pos < len(self.s) else None

    def consume(self, expected=None):
        if self.pos >= len(self.s):
            raise ValueError("Unexpected end of input")
        char = self.s[self.pos]
        self.pos += 1
        if expected and char != expected:
            raise ValueError(f"Expected '{expected}' but found '{char}' at position {self.pos - 1}")
        return char

    def parse_string(self):
        # Expects starting quote "
        self.consume('"')
        start = self.pos
        while self.pos < len(self.s) and self.peek() != '"':
            # Basic handling, assuming no complex escapes for subset requirement
            if self.peek() == '\\':
                self.consume('\\') # Skip escape sequence (e.g., \")
            self.pos += 1
        
        if self.pos >= len(self.s) or self.s[self.pos] != '"':
             raise ValueError("Unterminated string")

        value = self.s[start:self.pos]
        self.consume('"') # Consume closing quote
        return value

    def parse_number(self):
        start = self.pos
        while self.pos < len(self.s) and (self.peek().isdigit() or self.peek() == '-' or self.peek() == '.'):
            self.pos += 1
        
        num_str = self.s[start:self.pos]
        try:
            if '.' in num_str:
                return float(num_str)
            else:
                # Handle integers and potentially negative signs correctly parsed by the loop
                return int(num_str)
        except ValueError:
             raise ValueError(f"Invalid number format starting at position {start}")


    def parse_literal(self, literal, value):
        if self.s[self.pos:self.pos + len(literal)] == literal:
            self.pos += len(literal)
            return value
        raise ValueError(f"Expected '{literal}' but found something else at position {self.pos}")

    def parse_value(self):
        self.skip_whitespace()
        
        char = self.peek()
        if char is None:
            raise ValueError("Unexpected end of input while expecting a value")

        # 1. Object
        if char == '{':
            return self.parse_object()
        # 2. Array
        elif char == '[':
            return self.parse_array()
        # 3. String
        elif char == '"':
            return self.parse_string()
        # 4. Number (must check for negative sign first if it's not part of a literal keyword)
        elif char.isdigit() or char == '-':
             # We must ensure we are parsing a number, not starting a keyword like 'true' or 'false' which might start with letters/digits in some contexts, but JSON keywords are strict. 
             # Since numbers can start with '-', and literals can start with letters, this check is tricky.
             # Let's rely on parse_number to consume digits/dots after potential negative sign.
            return self.parse_number()
        # 5. Literals (true, false, null)
        elif char in ('t', 'f', 'n'):
            if self.s[self.pos:self.pos + 4] == "true":
                self.pos += 4
                return True
            elif self.s[self.pos:self.pos + 5] == "false":
                self.pos += 5
                return False
            elif self.s[self.pos:self.pos + 4] == "null":
                self.pos += 4
                return None
            else:
                 raise ValueError(f"Invalid literal starting at position {self.pos}. Found '{self.s[self.pos:]}'")

        raise ValueError(f"Unexpected character '{char}' at position {self.pos}. Cannot parse value.")


    def parse_array(self):
        self.consume('[') # Consume '['
        arr = []
        self.skip_whitespace()

        # Check for empty array '[]'
        if self.peek() == ']':
            self.consume(']')
            return arr

        while True:
            value = self.parse_value()
            arr.append(value)
            self.skip_whitespace()

            # After an element, expect comma or closing bracket
            next_char = self.peek()
            if next_char == ',':
                self.consume(',') # Consume ','
                self.skip_whitespace()
            elif next_char == ']':
                self.consume(']') # Consume ']'
                return arr
            else:
                raise ValueError(f"Expected ',' or ']' in array, found '{next_char}' at position {self.pos}")

    def parse_object(self):
        self.consume('{') # Consume '{'
        obj = {}
        self.skip_whitespace()

        # Check for empty object '{}'
        if self.peek() == '}':
            self.consume('}')
            return obj

        while True:
            # 1. Parse Key (must be a string)
            self.skip_whitespace()
            try:
                key = self.parse_string()
            except ValueError as e:
                 raise ValueError(f"Expected string key in object, found error near '{e}'")

            # 2. Expect colon separator
            self.skip_whitespace()
            self.consume(':') # Consume ':'

            # 3. Parse Value
            value = self.parse_value()
            obj[key] = value
            self.skip_whitespace()

            # After a pair, expect comma or closing brace
            next_char = self.peek()
            if next_char == ',':
                self.consume(',') # Consume ','
            elif next_char == '}':
                self.consume('}') # Consume '}'
                return obj
            else:
                raise ValueError(f"Expected ',' or '}}' in object, found '{next_char}' at position {self.pos}")


def parse(s):
    """
    Parses a JSON subset string s into corresponding Python data structures (dict, list, primitives).
    """
    parser = Parser(s)
    try:
        result = parser.parse_value()
        # Ensure all input was consumed after parsing the main value
        parser.skip_whitespace()
        if parser.pos != len(s):
            raise ValueError("Extra data found after complete JSON structure.")
        return result
    except ValueError as e:
        # Re-raise with context if needed, but for now, let it propagate test failures clearly
        raise e

