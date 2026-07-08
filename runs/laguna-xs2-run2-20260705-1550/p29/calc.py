
def evaluate(expr):
    expr = expr.replace(" ", "")
    pos = [0]  # use list for mutable reference in nested functions
    
    def current():
        if pos[0] >= len(expr):
            return None
        return expr[pos[0]]
    
    def consume():
        pos[0] += 1
    
    def number():
        start = pos[0]
        while pos[0] < len(expr) and (expr[pos[0]].isdigit() or expr[pos[0]] == '.'):
            pos[0] += 1
        return float(expr[start:pos[0]])
    
    def factor():
        if current() == '(':
            consume()
            val = expr_()
            if current() != ')':
                raise ValueError("Expected ')'")
            consume()
            return val
        elif current() == '-':
            consume()
            return -factor()
        else:
            return number()
    
    def term():
        val = factor()
        while current() in ('*', '/'):
            op = current()
            consume()
            right = factor()
            if op == '*':
                val = val * right
            else:
                val = val / right
        return val
    
    def expr_():
        val = term()
        while current() in ('+', '-'):
            op = current()
            consume()
            right = term()
            if op == '+':
                val = val + right
            else:
                val = val - right
        return val
    
    return expr_()