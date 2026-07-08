# Implement a simple recursive‑descent parser that respects operator precedence and handles parentheses and unary minus.
# The original implementation performed a left‑to‑right scan and ignored precedence, which caused all
# of the test failures.  The new version tokenises the input and walks the expression using
# the grammar below.

# Grammar
#   expr   : term ((+ | -) term)*
#   term   : factor ((* | /) factor)*
#   factor : (‘+’ | ‘-’)? (number | '(' expr ')')
#
# Numbers are parsed as floating point.  All operators are binary except the leading +/- which
# act as unary signs.  The parser consumes the entire string – any leftover characters will
# raise a ValueError.

import re
from typing import Optional

NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


class _Parser:
    def __init__(self, text: str):
        # Remove whitespace to simplify parsing.
        self.text = text.replace(" ", "")
        self.pos = 0
        self.length = len(self.text)

    def _peek(self) -> Optional[str]:
        if self.pos < self.length:
            return self.text[self.pos]
        return None

    def _consume(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def _consume_if(self, char: str) -> bool:
        if self._peek() == char:
            self._consume()
            return True
        return False

    def _parse_number(self) -> float:
        match = NUMBER_RE.match(self.text, self.pos)
        if not match:
            raise ValueError(f"Expected number at position {self.pos} in '{self.text}'")
        value = float(match.group(0))
        self.pos = match.end()
        return value

    def factor(self) -> float:
        # Handle unary plus/minus.
        if self._peek() in '+-':
            sign = 1
            if self._consume_if('-'):
                sign = -1
            else:
                self._consume()  # consume '+'
            return sign * self.factor()

        ch = self._peek()
        if ch == '(':
            self._consume()  # consume '('
            val = self.expr()
            if not self._consume_if(')'):
                raise ValueError(f"Missing closing parenthesis at position {self.pos} in '{self.text}'")
            return val
        # Must be a number.
        return self._parse_number()

    def term(self) -> float:
        value = self.factor()
        while True:
            ch = self._peek()
            if ch == '*':
                self._consume()
                value *= self.factor()
            elif ch == '/':
                self._consume()
                value /= self.factor()
            else:
                break
        return value

    def expr(self) -> float:
        value = self.term()
        while True:
            ch = self._peek()
            if ch == '+':
                self._consume()
                value += self.term()
            elif ch == '-':
                self._consume()
                value -= self.term()
            else:
                break
        return value

    def parse(self) -> float:
        value = self.expr()
        if self.pos != self.length:
            raise ValueError(f"Unexpected character '{self._peek()}' at position {self.pos} in '{self.text}'")
        return value


def evaluate(expr: str) -> float:
    """Evaluate a mathematical expression containing +, -, *, /, parentheses and unary minus.

    Parameters
    ----------
    expr: str
        The expression to evaluate.  Whitespace is ignored.

    Returns
    -------
    float
        The numeric result.
    """
    if not expr:
        return 0.0
    parser = _Parser(expr)
    return parser.parse()
