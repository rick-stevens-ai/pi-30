# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().

def evaluate(expr: str) -> float:
    """Evaluate arithmetic expression with proper precedence and unary operators.
    Implements the Shunting‑Yard algorithm (no eval()). Supports integers, floats,
    parentheses, and unary plus/minus.
    """
    # Strip whitespace
    s = expr.replace(" ", "")
    # Tokenise
    tokens = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in '+-*/()':
            # Determine unary plus/minus
            if ch in '+-':
                if i == 0 or s[i-1] in '+-*/(':
                    tokens.append('u' + ch)
                    i += 1
                    continue
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == '.':
            start = i
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                i += 1
            tokens.append(s[start:i])
        else:
            raise ValueError(f"Invalid character '{ch}' in expression")

    # Operator precedence (higher number = higher precedence)
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'u+': 3, 'u-': 3}
    # Stacks for the algorithm
    output: list[float] = []
    ops: list[str] = []

    for token in tokens:
        # Number
        if token.replace('.', '', 1).lstrip('-').isdigit():
            output.append(float(token))
        # Unary operators (right‑associative)
        elif token in ('u+', 'u-'):
            while ops and prec.get(ops[-1], 0) > prec[token]:
                output.append(ops.pop())
            ops.append(token)
        # Binary operators
        elif token in '+-*/':
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[token]:
                output.append(ops.pop())
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()  # discard '('
        else:
            raise ValueError(f"Unknown token {token}")

    while ops:
        if ops[-1] in '()':
            raise ValueError("Mismatched parentheses")
        output.append(ops.pop())

    # Evaluate RPN
    stack: list[float] = []
    for token in output:
        if isinstance(token, float):
            stack.append(token)
        else:
            if token == 'u-':
                val = stack.pop()
                stack.append(-val)
            elif token == 'u+':
                val = stack.pop()
                stack.append(+val)
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


