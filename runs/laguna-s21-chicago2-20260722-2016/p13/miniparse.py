# P13: a tiny JSON-subset parser (no eval, no json module).
# Supports null/true/false, ints, floats, strings, arrays, objects, nesting,
# and whitespace.
def parse(s):
    p = _Parser(s)
    p.skip_ws()
    value = p.parse_value()
    p.skip_ws()
    if p.i != len(p.s):
        raise ValueError("unexpected trailing data at %d" % p.i)
    return value


class _Parser:
    __slots__ = ("s", "i")

    def __init__(self, s):
        self.s = s
        self.i = 0

    def peek(self):
        if self.i < len(self.s):
            return self.s[self.i]
        return None

    def skip_ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\n\r":
            self.i += 1

    def expect(self, ch):
        if self.i >= len(self.s) or self.s[self.i] != ch:
            raise ValueError("expected %r at %d" % (ch, self.i))
        self.i += 1

    def parse_value(self):
        self.skip_ws()
        c = self.peek()
        if c is None:
            raise ValueError("unexpected end of input")
        if c == "n":
            return self.parse_literal("null", None)
        if c == "t":
            return self.parse_literal("true", True)
        if c == "f":
            return self.parse_literal("false", False)
        if c == '"':
            return self.parse_string()
        if c == "[":
            return self.parse_array()
        if c == "{":
            return self.parse_object()
        if c == "-" or c.isdigit():
            return self.parse_number()
        raise ValueError("unexpected character %r at %d" % (c, self.i))

    def parse_literal(self, literal, value):
        end = self.i + len(literal)
        if self.s[self.i:end] != literal:
            raise ValueError("invalid literal at %d" % self.i)
        self.i = end
        return value

    def parse_string(self):
        self.expect('"')
        out = []
        while True:
            if self.i >= len(self.s):
                raise ValueError("unterminated string")
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                return "".join(out)
            if c == "\\":
                self.i += 1
                if self.i >= len(self.s):
                    raise ValueError("unterminated escape")
                e = self.s[self.i]
                simple = {
                    '"': '"', "\\": "\\", "/": "/",
                    "b": "\b", "f": "\f", "n": "\n",
                    "r": "\r", "t": "\t",
                }
                if e in simple:
                    out.append(simple[e])
                    self.i += 1
                elif e == "u":
                    hex_digits = self.s[self.i + 1:self.i + 5]
                    if len(hex_digits) != 4:
                        raise ValueError("invalid unicode escape")
                    code = int(hex_digits, 16)
                    self.i += 5
                    out.append(chr(code))
                else:
                    raise ValueError("invalid escape \\%s" % e)
            else:
                out.append(c)
                self.i += 1

    def parse_number(self):
        start = self.i
        if self.peek() == "-":
            self.i += 1
        while self.i < len(self.s) and self.s[self.i].isdigit():
            self.i += 1
        is_float = False
        if self.i < len(self.s) and self.s[self.i] == ".":
            is_float = True
            self.i += 1
            while self.i < len(self.s) and self.s[self.i].isdigit():
                self.i += 1
        if self.i < len(self.s) and self.s[self.i] in "eE":
            is_float = True
            self.i += 1
            if self.i < len(self.s) and self.s[self.i] in "+-":
                self.i += 1
            while self.i < len(self.s) and self.s[self.i].isdigit():
                self.i += 1
        text = self.s[start:self.i]
        if not text or text == "-":
            raise ValueError("invalid number at %d" % start)
        return float(text) if is_float else int(text)

    def parse_array(self):
        self.expect("[")
        arr = []
        self.skip_ws()
        if self.peek() == "]":
            self.i += 1
            return arr
        while True:
            arr.append(self.parse_value())
            self.skip_ws()
            if self.peek() == ",":
                self.i += 1
                self.skip_ws()
                continue
            if self.peek() == "]":
                self.i += 1
                return arr
            raise ValueError("expected , or ] at %d" % self.i)

    def parse_object(self):
        self.expect("{")
        obj = {}
        self.skip_ws()
        if self.peek() == "}":
            self.i += 1
            return obj
        while True:
            self.skip_ws()
            if self.peek() != '"':
                raise ValueError("expected string key at %d" % self.i)
            key = self.parse_string()
            self.skip_ws()
            self.expect(":")
            value = self.parse_value()
            obj[key] = value
            self.skip_ws()
            if self.peek() == ",":
                self.i += 1
                self.skip_ws()
                continue
            if self.peek() == "}":
                self.i += 1
                return obj
            raise ValueError("expected , or } at %d" % self.i)