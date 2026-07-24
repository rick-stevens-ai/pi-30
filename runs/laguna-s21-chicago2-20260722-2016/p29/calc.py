# P29: recursive-descent arithmetic evaluator.
# Handles + - * / with correct precedence and left associativity,
# parentheses, unary minus, and integer/float literals.
# DO NOT use eval().
import re

def evaluate(expr):
    expr = expr.replace(" ", "")
    if not expr:
        return 0
    tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expr)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_expr():
        # term (('+' | '-') term)*
        val = parse_term()
        while peek() in ("+", "-"):
            op = advance()
            rhs = parse_term()
            val = val + rhs if op == "+" else val - rhs
        return val

    def parse_term():
        # factor (('*' | '/') factor)*
        val = parse_factor()
        while peek() in ("*", "/"):
            op = advance()
            rhs = parse_factor()
            if op == "*":
                val = val * rhs
            else:
                val = val / rhs
        return val

    def parse_factor():
        tok = peek()
        if tok == "-":
            advance()
            return -parse_factor()
        if tok == "+":
            advance()
            return parse_factor()
        if tok == "(":
            advance()
            val = parse_expr()
            if peek() == ")":
                advance()
            return val
        advance()
        return float(tok)

    return parse_expr()