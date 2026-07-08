# P29 SEED: arithmetic evaluator with proper precedence, parentheses, and unary operators.
# Implements a recursive‑descent parser without using eval().
# Supported:
#   - binary +, -, *, /
#   - parentheses ( )
#   - unary + and - (e.g., -5, -(2+3), 3*-2, 2--3)
# Numbers may be integers or floats.

def evaluate(expr: str) -> float:
    """Evaluate an arithmetic expression string.

    The parser follows the grammar:
        expr   ::= term (("+"|"-") term)*
        term   ::= factor (("*"|"/") factor)*
        factor ::= ("+"|"-") factor | number | "(" expr ")"

    Whitespace is ignored. Raises ``ValueError`` for malformed input.
    """
    # Remove whitespace for easier tokenisation
    expr = expr.replace(" ", "")

    import re
    # Token pattern captures numbers (int or float) and individual operators / parentheses
    token_pat = r"\d+\.?\d*|[+\-*/()]"
    tokens = re.findall(token_pat, expr)
    if not tokens:
        return 0.0

    # Index pointer closed over by the parser functions
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected: str = None):
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        cur = tokens[pos]
        if expected and cur != expected:
            raise ValueError(f"Expected '{expected}' but found '{cur}'")
        pos += 1
        return cur

    def parse_number(tok: str) -> float:
        # Convert token to float; token is guaranteed to match number pattern
        return float(tok)

    # Recursive‑descent parsing functions
    def parse_factor() -> float:
        tok = peek()
        if tok in ('+', '-'):
            # Unary plus/minus
            op = consume()
            val = parse_factor()
            return +val if op == '+' else -val
        if tok == '(':
            consume('(')
            val = parse_expr()
            consume(')')
            return val
        # Must be a number
        if tok is None:
            raise ValueError("Unexpected end of expression while parsing factor")
        return parse_number(consume())

    def parse_term() -> float:
        value = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_factor()
            if op == '*':
                value *= right
            else:
                value /= right
        return value

    def parse_expr() -> float:
        value = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            if op == '+':
                value += right
            else:
                value -= right
        return value

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError(f"Unexpected token '{peek()}' at position {pos}")
    return result

