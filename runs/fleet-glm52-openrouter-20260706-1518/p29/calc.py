# P29: recursive-descent arithmetic evaluator.
# evaluate(expr) handles + - * / ( ) with correct precedence and
# associativity, integer and float, unary minus. No eval() allowed.
def evaluate(expr):
    expr = expr.replace(" ", "")
    pos = [0]

    def peek():
        return expr[pos[0]] if pos[0] < len(expr) else None

    def advance():
        ch = expr[pos[0]]
        pos[0] += 1
        return ch

    def parse_number():
        start = pos[0]
        while pos[0] < len(expr) and (expr[pos[0]].isdigit() or expr[pos[0]] == "."):
            pos[0] += 1
        return float(expr[start:pos[0]])

    def parse_primary():
        ch = peek()
        if ch == "(":
            advance()  # consume '('
            val = parse_expr()
            if peek() == ")":
                advance()  # consume ')'
            return val
        if ch == "-":
            advance()
            return -parse_unary()
        if ch == "+":
            advance()
            return parse_unary()
        return parse_number()

    def parse_unary():
        ch = peek()
        if ch == "-":
            advance()
            return -parse_unary()
        if ch == "+":
            advance()
            return parse_unary()
        return parse_primary()

    def parse_term():
        val = parse_unary()
        while peek() in ("*", "/"):
            op = advance()
            rhs = parse_unary()
            if op == "*":
                val *= rhs
            else:
                val /= rhs
        return val

    def parse_expr():
        val = parse_term()
        while peek() in ("+", "-"):
            op = advance()
            rhs = parse_term()
            if op == "+":
                val += rhs
            else:
                val -= rhs
        return val

    if not expr:
        return 0
    return parse_expr()
