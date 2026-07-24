def evaluate(expr):
    expr = expr.replace(" ", "")
    pos = 0
    n = len(expr)

    def peek():
        return expr[pos] if pos < n else ''

    def consume(ch=None):
        nonlocal pos
        if ch is not None and peek() != ch:
            raise ValueError(f"Expected {ch}")
        c = peek()
        pos += 1
        return c

    def parse_number():
        start = pos
        if peek() == '.':
            # handle numbers starting with dot? not needed but safe
            pass
        while peek().isdigit() or peek() == '.':
            consume()
        if start == pos:
            raise ValueError("Expected number")
        return float(expr[start:pos])

    def parse_factor():
        if peek() == '-':
            consume('-')
            val = parse_factor()
            return -val
        elif peek() == '+':
            consume('+')
            return parse_factor()
        elif peek() == '(':
            consume('(')
            val = parse_expr()
            consume(')')
            return val
        else:
            return parse_number()

    def parse_term():
        val = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            rhs = parse_factor()
            if op == '*':
                val *= rhs
            else:
                val /= rhs
        return val

    def parse_expr():
        val = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            rhs = parse_term()
            if op == '+':
                val += rhs
            else:
                val -= rhs
        return val

    result = parse_expr()
    if pos != n:
        raise ValueError("Unexpected trailing chars")
    return result
