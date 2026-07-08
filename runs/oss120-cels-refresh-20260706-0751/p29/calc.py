# Updated evaluate function with proper operator precedence, parentheses, and unary handling.
# Implements a recursive descent parser without using eval().

def evaluate(expr):
    """Evaluate an arithmetic expression containing +, -, *, /, parentheses and unary +/-.
    Returns a float. Raises ValueError for malformed expressions.
    """
    # Remove whitespace
    s = expr.replace(" ", "")
    # Index pointer
    i = 0

    def peek():
        return s[i] if i < len(s) else None

    def consume(char=None):
        nonlocal i
        if char and peek() != char:
            raise ValueError(f"Expected '{char}' at position {i}")
        i += 1

    def parse_number():
        nonlocal i
        start = i
        # optional leading digits, optional decimal point and fractional part
        while peek() and (peek().isdigit() or peek() == '.'):
            i += 1
        if start == i:
            raise ValueError(f"Number expected at position {i}")
        return float(s[start:i])

    # Grammar implementation
    def parse_factor():
        # factor -> ('+'|'-') factor | number | '(' expr ')'
        if peek() in ('+', '-'):
            sign = 1
            if peek() == '-':
                sign = -1
            consume()
            return sign * parse_factor()
        elif peek() == '(':
            consume('(')
            val = parse_expr()
            if peek() != ')':
                raise ValueError(f"Missing ')' at position {i}")
            consume(')')
            return val
        else:
            return parse_number()

    def parse_term():
        # term -> factor (( '*' | '/' ) factor)*
        val = parse_factor()
        while peek() in ('*', '/'):
            op = peek()
            consume()
            right = parse_factor()
            if op == '*':
                val *= right
            else:
                val /= right
        return val

    def parse_expr():
        # expr -> term (( '+' | '-' ) term)*
        val = parse_term()
        while peek() in ('+', '-'):
            op = peek()
            consume()
            right = parse_term()
            if op == '+':
                val += right
            else:
                val -= right
        return val

    result = parse_expr()
    if i != len(s):
        raise ValueError(f"Unexpected character at position {i}: '{peek()}'")
    return result

