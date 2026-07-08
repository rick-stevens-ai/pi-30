# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().
def evaluate(expr):
    expr = expr.replace(" ", "")
    # naive: split on operators left to right, ignore precedence & parens
    import re
    tokens = re.findall(r"\d+\.?\d*|[+\-*/]", expr)
    if not tokens:
        return 0
    acc = float(tokens[0])
    i = 1
    while i < len(tokens) - 1:
        op = tokens[i]; val = float(tokens[i+1])
        if op == "+": acc += val
        elif op == "-": acc -= val
        elif op == "*": acc *= val
        elif op == "/": acc /= val
        i += 2
    return acc
