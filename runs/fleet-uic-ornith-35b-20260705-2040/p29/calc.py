def evaluate(expr):
    expr = expr.replace(" ", "")
    if not expr:
        return 0.0

    # Tokenize: + - * / ( ) and numbers.
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit() or c == '.':
            j = i + 1
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(('NUM', float(expr[i:j])))
            i = j
        elif c == '-':
            # unary minus if this is the first token, preceded by '(', or an operator
            if not tokens or tokens[-1][0] in ('LPAREN', 'OP', 'UNARY'):
                tokens.append(('UNARY', '-'))
            else:
                tokens.append(('OP', '-'))
            i += 1
        elif c == '+':
            # unary plus if it can't possibly be binary (preceded by start/ '(' / operator)
            if not tokens or tokens[-1][0] in ('LPAREN', 'OP'):
                pass  # skip unary plus silently — it doesn't change the value
            else:
                tokens.append(('OP', '+'))
            i += 1
        elif c == '*':
            tokens.append(('OP', '*'))
            i += 1
        elif c == '/':
            tokens.append(('OP', '/'))
            i += 1
        elif c == '(':
            tokens.append(('LPAREN', '('))
            i += 1
        elif c == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
        else:
            raise ValueError(f"Unexpected character '{c}'")
    assert i == len(expr)

    pos = [0]

    def peek():
        if pos[0] < len(tokens):
            return tokens[pos[0]]
        return None

    def advance():
        tok = tokens[pos[0]]
        pos[0] += 1
        return tok

    def parse_expr():
        """expr = term (('+'|'-') term)*"""
        left = parse_term()
        while True:
            t = peek()
            if t and t[0] == 'OP' and t[1] in ('+', '-'):
                op = advance()[1]
                right = parse_term()
                left = (left + right) if op == '+' else (left - right)
            else:
                break
        return left

    def parse_term():
        """term = factor (('*'|'/') factor)*"""
        left = parse_factor()
        while True:
            t = peek()
            if t and t[0] == 'OP' and t[1] in ('*', '/'):
                op = advance()[1]
                right = parse_factor()
                left = (left * right) if op == '*' else (left / right)
            else:
                break
        return left

    def parse_factor():
        """factor = NUMBER | '-' factor | '(' expr ')'"""
        t = peek()
        # unary minus: -5, -(expr)
        if t and t[0] == 'UNARY':
            advance()  # consume
            return -parse_factor()
        # number
        if t and t[0] == 'NUM':
            advance()
            return t[1]
        # parenthesized
        if t and t[0] == 'LPAREN':
            advance()  # skip '('
            val = parse_expr()
            rp = peek()
            if (rp is None or rp[0] != 'RPAREN'):
                raise ValueError("Expected closing ')' but got " + str(rp))
            advance()  # skip ')'
            return val
        raise ValueError(f"Unexpected token: {t}")

    result = parse_expr()
    if pos[0] < len(tokens):
        raise ValueError(f"Unprocessed input at token {pos[0]}: {tokens[pos[0]]}")
    return result
