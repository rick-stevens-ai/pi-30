import re

def evaluate(expr):
    # Tokenize: numbers (including floats), operators, and parentheses
    tokens = re.findall(r"\d*\.\d+|\d+|[+\-*/()]", expr.replace(" ", ""))
    token_iter = iter(tokens)
    current_token = next(token_iter, None)

    def advance():
        nonlocal current_token
        current_token = next(token_iter, None)

    def parse_expression():
        node = parse_term()
        while current_token in ("+", "-"):
            op = current_token
            advance()
            right = parse_term()
            if op == "+":
                node += right
            else:
                node -= right
        return node

    def parse_term():
        node = parse_factor()
        while current_token in ("*", "/"):
            op = current_token
            advance()
            right = parse_factor()
            if op == "*":
                node *= right
            else:
                node /= right
        return node

    def parse_factor():
        nonlocal current_token
        if current_token == "-":
            advance()
            return -parse_factor()
        elif current_token == "+":
            advance()
            return parse_factor()
        elif current_token == "(":
            advance()
            node = parse_expression()
            if current_token == ")":
                advance()
            else:
                raise ValueError(f"Expected ')' but found {current_token}")
            return node
        else:
            if current_token is not None:
                val = float(current_token)
                advance()
                return val
            else:
                raise ValueError("Unexpected end of expression")

    result = parse_expression()
    return result
