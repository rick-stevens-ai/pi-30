def evaluate(expr):
    expr = expr.replace(" ", "")
    if not expr:
        return 0.0
    
    # Tokenize the expression
    import re
    tokens = re.findall(r"\d+\.?\d*|[+\-*/()]|\[-+]?\d+\.?\d*", expr)
    
    # Remove empty tokens
    tokens = [t for t in tokens if t]
    
    # Parse the expression
    def parse_expression():
        result = parse_term()
        while tokens and tokens[0] in '+-':
            op = tokens.pop(0)
            right = parse_term()
            if op == '+':
                result += right
            else:
                result -= right
        return result
    
    def parse_term():
        result = parse_factor()
        while tokens and tokens[0] in '*/':
            op = tokens.pop(0)
            right = parse_factor()
            if op == '*':
                result *= right
            else:
                result /= right
        return result
    
    def parse_factor():
        # Handle unary minus and plus
        if tokens[0] in '+-':
            op = tokens.pop(0)
            factor = parse_factor()
            return -factor if op == '-' else factor
        return parse_atom()
    
    def parse_atom():
        if tokens[0] == '(':
            tokens.pop(0)  # Remove '('
            result = parse_expression()
            if tokens[0] != ')':
                raise ValueError("Mismatched parentheses")
            tokens.pop(0)  # Remove ')'
            return result
        else:
            # Number token
            return float(tokens.pop(0))
    
    # Parse the expression
    return parse_expression()
