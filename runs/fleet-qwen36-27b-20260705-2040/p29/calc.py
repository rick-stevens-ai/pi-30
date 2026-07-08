def evaluate(expr):
    expr = expr.replace(" ", "")
    pos = [0]  # mutable index into expr

    def peek():
        if pos[0] < len(expr):
            return expr[pos[0]]
        return None

    def advance():
        ch = expr[pos[0]]
        pos[0] += 1
        return ch

    # factor -> ('-'|'+') factor | NUMBER | '(' expr ')'
    def factor():
        ch = peek()
        if ch == '-':
            advance()
            return -factor()
        if ch == '+':
            advance()
            return factor()
        if ch == '(':
            advance()  # consume '('
            val = expr_parse()
            if peek() == ')':
                advance()  # consume ')'
            return val
        # number
        start = pos[0]
        while pos[0] < len(expr) and (expr[pos[0]].isdigit() or expr[pos[0]] == '.'):
            pos[0] += 1
        return float(expr[start:pos[0]])

    # term -> factor (('*'|'/') factor)*
    def term():
        val = factor()
        while peek() in ('*', '/'):
            op = advance()
            right = factor()
            if op == '*':
                val *= right
            else:
                val /= right
        return val

    # expr -> term (('+'|'-') term)*
    def expr_parse():
        val = term()
        while peek() in ('+', '-'):
            op = advance()
            right = term()
            if op == '+':
                val += right
            else:
                val -= right
        return val

    return expr_parse()
