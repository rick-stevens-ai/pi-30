# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().
def evaluate(expr):
    s = expr.replace(" ", "")
    n = len(s)
    pos = 0

    def parse_expr():
        nonlocal pos
        val = parse_term()
        while pos < n and s[pos] in '+-':
            op = s[pos]; pos+=1; rhs=parse_term()
            if op == '+':
                val += rhs
            else:
                val -= rhs
        return val

    def parse_term():
        nonlocal pos
        val = parse_factor()
        while pos < n and s[pos] in '*/':
            op=s[pos]; pos+=1
            rhs=parse_factor()
            if op=='*':
                val*=rhs
            else:  # '/'
                val/=rhs
        return val

    def parse_factor():
        nonlocal pos
        sign=1
        while pos<n and s[pos] in '+-':
            if s[pos]=='-': sign*=-1
            pos+=1
        val = parse_primary()
        return sign*val

    def parse_primary():
        nonlocal pos
        if pos>=n:
            raise Exception("Unexpected end of input")
        c=s[pos]
        if c=='(':
            pos+=1
            val=parse_expr()
            if pos>=n or s[pos]!=')':
                raise Exception("Mismatched parentheses")
            pos+=1
            return val
        elif c.isdigit() or c=='.':
            start=pos
            while pos<n and (s[pos].isdigit() or s[pos]=='.'):
                pos+=1
            num_str=s[start:pos]
            return float(num_str)
        else:
            raise Exception(f"Unexpected character {c}")
    result = parse_expr()
    if pos!=n:
        raise Exception("Extra characters after parsing")
    return result