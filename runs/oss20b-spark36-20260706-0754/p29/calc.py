# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().
def evaluate(expr):
    import re
    expr = expr.replace(" ", "")
    pos=[0]
    s=expr

    def parse_factor():
        # handle signs and parentheses or numbers
        sign = 1
        while pos[0] < len(s) and s[pos[0]] in "+-":
            if s[pos[0]] == '-':
                sign *= -1
            pos[0] += 1

        if pos[0] >= len(s):
            raise ValueError("Unexpected end")
        if s[pos[0]] == '(':
            pos[0] += 1
            val = parse_expr()
            if pos[0] >= len(s) or s[pos[0]] != ')':
                raise ValueError("Expected ')'")
            pos[0] += 1
        else:
            m = re.match(r'\d+\.?\d*', s[pos[0]:])
            if not m:
                raise ValueError(f"Invalid number at {pos[0]}")
            val = float(m.group())
            pos[0] += len(m.group())
        return sign * val

    def parse_term():
        val = parse_factor()
        while pos[0] < len(s) and s[pos[0]] in '*/':
            op = s[pos[0]]
            pos[0] += 1
            right = parse_factor()
            if op == '*':
                val *= right
            else:
                val /= right
        return val

    def parse_expr():
        val = parse_term()
        while pos[0] < len(s) and s[pos[0]] in '+-':
            op = s[pos[0]]
            pos[0] += 1
            right = parse_term()
            if op == '+':
                val += right
            else:
                val -= right
        return val

    result = parse_expr()
    if pos[0] != len(s):
        raise ValueError("Unexpected characters")
    return result