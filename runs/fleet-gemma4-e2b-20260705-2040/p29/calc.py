import re

# --- Tokenization ---

def tokenize(expr):
    """Tokenizes the expression string into numbers, operators, and parentheses."""
    # Pattern to match numbers (integers or floats), operators, and parentheses.
    token_specification = [
        ('NUMBER', r'[-]?\d+\.?\d*'),  # Numbers: optional sign, digits, optional decimal part
        ('OP', r'[+\-*/]'),           # Operators
        ('LPAREN', r'\('),            # Left parenthesis
        ('RPAREN', r'\)'),            # Right parenthesis
        ('SKIP', r'[ \t]+'),          # Skip whitespace
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, expr):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, value))
    return tokens

# --- Recursive Descent Parsing ---

class Calculator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None, expected_value=None):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of expression")
        token = self.tokens[self.pos]
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Expected token type {expected_type}, got {token[0]} ('{token[1]}')")
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f"Expected token value '{expected_value}', got '{token[1]}'")
        self.pos += 1
        return token

    def parse_primary(self):
        """Handles numbers and parenthesized expressions."""
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of expression while parsing primary")

        token_type, token_value = token

        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return float(token_value)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            result = self.parse_expression()
            self.consume('RPAREN')
            return result
        else:
            raise SyntaxError(f"Unexpected token in primary expression: {token}")

    def parse_term(self):
        """Handles multiplication and division."""
        result = self.parse_primary()

        while self.peek() and self.peek()[0] == 'OP':
            op_type, op_value = self.peek()
            if op_value in ('*', '/'):
                self.consume('OP')
                right = self.parse_primary()
                if op_value == '*':
                    result *= right
                elif op_value == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    result /= right
            else:
                break
        return result

    def parse_expression(self):
        """Handles addition and subtraction."""
        result = self.parse_term()

        while self.peek() and self.peek()[0] == 'OP':
            op_type, op_value = self.peek()
            if op_value in ('+', '-'):
                self.consume('OP')
                right = self.parse_term()
                if op_value == '+':
                    result += right
                elif op_value == '-':
                    result -= right
            else:
                break
        return result

    def parse(self):
        """Starts the parsing process."""
        result = self.parse_expression()
        if self.pos != len(self.tokens):
             raise SyntaxError("Expression not fully consumed")
        return result


def evaluate(expr):
    """Evaluates a mathematical expression string respecting precedence and parentheses."""
    if not expr:
        return 0.0

    tokens = tokenize(expr)
    calculator = Calculator(tokens)
    return calculator.parse()