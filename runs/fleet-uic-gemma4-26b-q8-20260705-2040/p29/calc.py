import re

def evaluate(expr):
    """Evaluates an arithmetic expression with +, -, *, / and parentheses.
    Supports unary minus. Does not use eval().
    """
    expr = expr.replace(" ", "")
    if not expr:
        return 0.0

    # Tokenize the expression into numbers, operators, and parentheses
    tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expr)
    pos = 0

    def peek():
        nonlocal pos
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        token = peek()
        if expected and token != expected:
            raise ValueError(f"Expected {expected}, but got {token}")
        pos += 1
        return token

    def parse_expr():
        node = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            if op == '+':
                node += right
            else:
                node -= right
        return node

    def parse_term():
        node = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_factor()
            if op == '*':
                node *= right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                node /= right
        return node

    def parse_factor():
        token = peek()
        if token == '-':
            consume('-')
            return -parse_factor()
        elif token == '+':
            consume('+')
            return parse_factor()
        else:
            return parse_primary()

    def parse_primary():
        token = peek()
        if token == '(':
            consume('(')
            node = parse_expr()
            consume(')')
            return node
        elif token is not None and re.match(r"\d+\.?\d*", token):
            return float(consume())
        else:
            raise ValueError(f"Unexpected token: {token}")

    result = parse_expr()
    if pos < len(tokens):
        raise ValueError(f"Trailing tokens at position {pos}: {tokens[pos:]}")
    return result
