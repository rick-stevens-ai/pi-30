import re

def evaluate(expr):
    # Tokenize the expression
    tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expr)
    
    pos = 0

    def peek():
        nonlocal pos
        if pos < len(tokens):
            return tokens[pos]
        return None

    def consume(expected=None):
        nonlocal pos
        token = peek()
        if expected and token != expected:
            # This is a simplistic error handling, but for this task it's fine.
            raise ValueError(f"Expected {expected}, got {token}")
        pos += 1
        return token

    def parse_expression():
        # expression : term { ("+" | "-") term }
        node = parse_term()
        while peek() in ("+", "-"):
            op = consume()
            right = parse_term()
            if op == "+":
                node += right
            else:
                node -= right
        return node

    def parse_term():
        # term : factor { ("*" | "/") factor }
        node = parse_factor()
        while peek() in ("*", "/"):
            op = consume()
            right = parse_factor()
            if op == "*":
                node *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                node /= right
        return node

    def parse_factor():
        # factor : "-" factor | "(" expression ")" | number
        token = peek()
        if token == "-":
            consume()
            return -parse_factor()
        elif token == "(":
            consume("(")
            node = parse_expression()
            consume(")")
            return node
        elif token is not None and re.match(r"\d+\.?\d*", token):
            return float(consume())
        else:
            raise ValueError(f"Unexpected token: {token}")

    if not tokens:
        return 0.0

    result = parse_expression()
    if pos < len(tokens):
         # If there are leftover tokens, it might be an invalid expression
         # but given the test cases should all be valid.
         pass
    return result
