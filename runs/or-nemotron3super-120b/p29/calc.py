# P29 iterate-until-green: a shunting-yard / recursive-descent arithmetic
# evaluator. evaluate(expr) handles + - * / ( ) with correct precedence and
# associativity, integer and float, unary minus. Seed only does left-to-right
# single-op. No eval() allowed. Verdict = pytest exit code.
import re

def evaluate(expr):
    """
    Evaluate an arithmetic expression with + - * / ( ) and unary minus.
    Uses the shunting-yard algorithm to convert to RPN, then evaluates.
    """
    # Remove all whitespace
    expr = expr.replace(" ", "")
    if not expr:
        return 0

    # Tokenize: numbers (including floats), operators, parentheses
    token_pattern = r'\d+\.?\d*|[+\-*/()]'
    tokens = re.findall(token_pattern, expr)
    if not tokens:
        return 0

    # Shunting-yard algorithm
    output = []      # output queue
    stack = []       # operator stack
    # Precedence and associativity
    precedence = {
        'u': 4,   # unary minus (right-associative)
        '*': 3,   # multiplication (left)
        '/': 3,   # division (left)
        '+': 2,   # addition (left)
        '-': 2,   # subtraction (left)
    }
    associativity = {
        'u': 'right',
        '*': 'left',
        '/': 'left',
        '+': 'left',
        '-': 'left',
    }

    # Helper to determine if a token is an operator (including unary minus)
    def is_op(token):
        return token in precedence

    # We need to distinguish unary minus from binary minus.
    # We'll keep track of the last token type to decide.
    # Possible last token types: None (start), 'num', 'op', '(' , ')'
    last_type = None  # None, 'num', 'op', '(', ')'

    for token in tokens:
        # If token is a number, add to output
        if re.match(r'\d+\.?\d*', token):
            output.append(float(token))
            last_type = 'num'
        elif token == '(':
            stack.append(token)
            last_type = '('
        elif token == ')':
            # Pop operators until '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()  # Discard the '('
            last_type = ')'
        else:  # token is an operator + - * /
            # Determine if this '-' is unary
            if token == '-':
                if last_type in (None, 'op', '('):
                    token = 'u'  # unary minus
                else:
                    token = '-'  # binary minus
            # Now token is either '+', '-', '*', '/', or 'u'
            o1 = token
            p1 = precedence[o1]
            a1 = associativity[o1]
            # While there is an operator at the top of the stack with greater precedence,
            # or equal precedence and left-associative, pop it to output.
            while stack and stack[-1] != '(':
                o2 = stack[-1]
                if o2 not in precedence:
                    break  # should not happen
                p2 = precedence[o2]
                a2 = associativity[o2]
                if (a1 == 'left' and p1 <= p2) or (a1 == 'right' and p1 < p2):
                    output.append(stack.pop())
                else:
                    break
            stack.append(o1)
            last_type = 'op'

    # Pop any remaining operators to output
    while stack:
        op = stack.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses")
        output.append(op)

    # Evaluate the RPN expression
    stack = []
    for token in output:
        if isinstance(token, float):
            stack.append(token)
        elif token == 'u':
            operand = stack.pop()
            stack.append(-operand)
        else:  # binary operator
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