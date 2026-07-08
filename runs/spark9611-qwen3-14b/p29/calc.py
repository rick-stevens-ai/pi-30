import re

def evaluate(expr):
    tokens = tokenize(expr)
    parser = Parser(tokens)
    return parser.parse()

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i] in '()+-*/':
            tokens.append(expr[i])
            i += 1
        elif expr[i].isdigit() or expr[i] == '.':
            # Parse number
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            raise ValueError(f"Invalid character: {expr[i]}")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        left = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('+', '-'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            if op == '+':
                left += right
            elif op == '-':
                left -= right
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('*', '/'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_factor()
            if op == '*':
                left *= right
            elif op == '/':
                left /= right
        return left

    def parse_factor(self):
        # Handle unary minus
        count = 0
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '-':
            count += 1
            self.pos += 1
        val = self.parse_primary()
        if count % 2 == 1:
            val = -val
        return val

    def parse_primary(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == '(':
            self.pos += 1
            val = self.parse_expression()
            if self.pos < len(self.tokens) and self.tokens[self.pos] == ')':
                self.pos += 1
            else:
                raise ValueError("Expected ')'")
            return val
        elif self.pos < len(self.tokens) and (self.tokens[self.pos].isdigit() or self.tokens[self.pos] == '.'):
            val = float(self.tokens[self.pos])
            self.pos += 1
            return val
        else:
            raise ValueError(f"Unexpected token: {self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'}")