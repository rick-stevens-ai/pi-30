# P29: Shunting-yard arithmetic evaluator
# Handles +, -, *, /, parentheses, unary minus, correct precedence
def evaluate(expr):
    expr = expr.replace(" ", "")
    if not expr:
        return 0
    
    # Tokenize
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit() or c == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            tokens.append(c)
            i += 1
    
    # Shunting-yard to RPN
    output = []
    ops = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3}  # u- is unary minus
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L'}
    
    def apply_op(op):
        if op == 'u-':
            a = output.pop()
            output.append(-a)
        else:
            b = output.pop()
            a = output.pop()
            if op == '+': output.append(a + b)
            elif op == '-': output.append(a - b)
            elif op == '*': output.append(a * b)
            elif op == '/': output.append(a / b)
    
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.replace('.', '').isdigit() or (t and t[0].isdigit()):
            output.append(float(t))
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                apply_op(ops.pop())
            if ops:
                ops.pop()  # Remove '('
        elif t in '+-*/':
            # Check for unary minus/plus
            is_unary = (i == 0 or tokens[i-1] in '+-*/(')
            if t == '-' and is_unary:
                ops.append('u-')
            else:
                while ops and ops[-1] not in '(':
                    top = ops[-1]
                    top_prec = precedence.get(top, 0)
                    curr_prec = precedence.get(t, 0)
                    if top_prec > curr_prec or \
                       (top_prec == curr_prec and associativity[t] == 'L'):
                        apply_op(ops.pop())
                    else:
                        break
                ops.append(t)
        i += 1
    
    while ops:
        apply_op(ops.pop())
    
    return output[0] if output else 0