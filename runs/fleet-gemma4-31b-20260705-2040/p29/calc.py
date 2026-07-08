import re

def evaluate(expr):
    expr = expr.replace(" ", "")
    pos = 0

    def peek():
        nonlocal pos
        return expr[pos] if pos < len(expr) else None

    def consume():
        nonlocal pos
        char = peek()
        pos += 1
        return char

    def parse_expression():
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
            else:
                node /= right
        return node

    def parse_factor():
        char = peek()
        if char == '+':
            consume()
            return parse_factor()
        if char == '-':
            consume()
            return -parse_factor()
        if char == '(':
            consume() # consume '('
            node = parse_expression()
            consume() # consume ')'
            return node
        
        start_pos = pos
        while peek() and (peek().isdigit() or peek() == '.'):
            consume()
        
        return float(expr[start_pos:pos])

    return parse_expression()
