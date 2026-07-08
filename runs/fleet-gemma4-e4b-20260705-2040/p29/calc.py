import re

def tokenize(expr):
    """Tokenizes the input expression, separating numbers, operators, and parentheses."""
    # Pattern matches numbers (integers or floats) OR single character tokens (+, -, *, /, (, ))
    return re.findall(r'(\d+\.?\d*|\.\d+|\+|-|\*|/|\(|\))', expr)

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        raise EOFError("Unexpected end of expression")

def parse_expression(stream):
    """Top-level parsing function."""
    return parse_sum(stream)

def parse_sum(stream):
    """Handles Addition (+) and Subtraction (-) (Lowest precedence)."""
    left = parse_product(stream)
    while True:
        op = stream.peek()
        if op in ('+', '-'):
            stream.consume() # Consume operator
            right = parse_product(stream)
            if op == '+':
                left += right
            else: # op == '-'
                left -= right
        else:
            break
    return left

def parse_product(stream):
    """Handles Multiplication (*) and Division (/) (Medium precedence)."""
    left = parse_factor(stream)
    while True:
        op = stream.peek()
        if op in ('*', '/'):
            stream.consume() # Consume operator
            right = parse_factor(stream)
            if op == '*':
                left *= right
            else: # op == '/'
                # Basic division check
                if abs(right) < 1e-9:
                    raise ZeroDivisionError("Division by zero")
                left /= right
        else:
            break
    return left

def parse_factor(stream):
    """Handles numbers, parentheses, and unary operations (Highest precedence)."""
    token = stream.peek()

    # 1. Handle Parentheses
    if token == '(':
        stream.consume() # Consume '('
        result = parse_sum(stream)
        # Must close parenthesis
        if stream.peek() != ')':
            raise ValueError("Mismatched parentheses: expected ')'")
        stream.consume() # Consume ')'
        return result

    # 2. Handle Unary Operators (+/-)
    elif token in ('+', '-'):
        op = stream.consume()
        sign = 1 if op == '+' else -1
        try:
            next_factor = parse_factor(stream) # Recurse to get the value
            return next_factor * sign
        except EOFError:
             raise ValueError("Invalid expression after unary operator")

    # 3. Handle Numbers (Base case)
    elif token is not None and re.match(r'^-?\d+\.?\d*$', token):
        try:
            return float(stream.consume())
        except ValueError:
             raise ValueError(f"Invalid number format: {token}")

    # 4. Error case
    else:
        if token is None:
            raise EOFError("Unexpected end of input")
        raise ValueError(f"Unexpected token encountered: {token}")


def evaluate(expr):
    """Evaluates the mathematical expression string."""
    if not expr:
        return 0.0

    # Pre-process to handle simple cases like "5." -> "5.0" if needed, though float() handles it.
    
    tokens = tokenize(expr)
    stream = TokenStream(tokens)
    
    try:
        result = parse_expression(stream)
        return result
    except (EOFError, ValueError, ZeroDivisionError) as e:
        # Re-raise specific errors for testing consistency if needed, or just handle them.
        raise e

