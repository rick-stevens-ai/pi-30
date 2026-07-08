# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().

def evaluate(expr):
    """Evaluate arithmetic expression with +, -, *, /, (), unary minus, floats."""
    expr = expr.replace(" ", "")
    if not expr:
        return 0

    # Tokenize: numbers (int/float), operators, parentheses
    import re
    tokens = re.findall(r'\d+\.?\d*|\.\d+|[+\-*/()]', expr)
    if not tokens:
        return 0

    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        if pos >= len(tokens):
            return None
        tok = tokens[pos]
        if expected and tok != expected:
            raise ValueError(f"Expected {expected}, got {tok}")
        pos += 1
        return tok

    def parse_expr():
        """expr := term (('+' | '-') term)*"""
        val = parse_term()
        while True:
            tok = peek()
            if tok == '+':
                consume('+')
                val += parse_term()
            elif tok == '-':
                consume('-')
                val -= parse_term()
            else:
                break
        return val

    def parse_term():
        """term := factor (('*' | '/') factor)*"""
        val = parse_factor()
        while True:
            tok = peek()
            if tok == '*':
                consume('*')
                val *= parse_factor()
            elif tok == '/':
                consume('/')
                val /= parse_factor()
            else:
                break
        return val

    def parse_factor():
        """factor := number | '(' expr ')' | '-' factor"""
        tok = peek()
        if tok == '-':
            consume('-')
            return -parse_factor()
        elif tok == '(':
            consume('(')
            val = parse_expr()
            consume(')')
            return val
        else:
            # number
            tok = consume()
            return float(tok)

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError(f"Unexpected token at position {pos}: {peek()}")
    return result
