# Recursive descent parser for arithmetic expressions
# Handles + - * / ( ) with correct precedence, unary minus

def evaluate(expr):
    expr = expr.replace(" ", "")
    if not expr:
        return 0.0
    
    # Tokenize the expression
    import re
    tokens = re.findall(r"\d+\.?\d*|[+\-*/()]", expr)
    
    # Add implicit multiplication for cases like "2(3+4)"
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == ')' and tokens[i+1] == '(':
            tokens.insert(i+1, '*')
        elif tokens[i].isdigit() or tokens[i][-1] == '.':
            if tokens[i+1] == '(':
                tokens.insert(i+1, '*')
        i += 1
    
    # Parser state
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0
            
        def peek(self):
            if self.pos >= len(self.tokens):
                return None
            return self.tokens[self.pos]
        
        def consume(self):
            token = self.peek()
            if token is not None:
                self.pos += 1
            return token
        
        def parse_expression(self):
            result = self.parse_term()
            while self.peek() in ['+', '-']:
                op = self.consume()
                right = self.parse_term()
                if op == '+':
                    result += right
                else:
                    result -= right
            return result
        
        def parse_term(self):
            result = self.parse_factor()
            while self.peek() in ['*', '/']:
                op = self.consume()
                right = self.parse_factor()
                if op == '*':
                    result *= right
                else:
                    result /= right
            return result
        
        def parse_factor(self):
            token = self.peek()
            
            # Handle unary minus or plus
            if token in ['+', '-']:
                op = self.consume()
                factor = self.parse_factor()
                return -factor if op == '-' else factor
            else:
                # Handle parentheses
                if token == '(':
                    self.consume()  # consume '('
                    result = self.parse_expression()
                    if self.peek() != ')':
                        raise ValueError("Mismatched parentheses")
                    self.consume()  # consume ')'
                    return result
                
                # Handle numbers and variables (treat as numbers)
                elif self.is_number(token):
                    self.consume()
                    try:
                        return int(token) if '.' not in token else float(token)
                    except ValueError:
                        raise ValueError(f"Invalid number: {token}")
                
                # Handle implicit multiplication (e.g., 2pi or 2(3+4))
                elif self.is_implicit_mul(token):
                    self.consume()
                    return float('nan')  # Shouldn't reach here
                
                else:
                    raise ValueError(f"Unexpected token: {token}")
        
        def is_number(self, token):
            if not token or (token[0] == '-' and len(token) == 1):
                return False
            return bool(re.match(r"^-?\d+\.?\d*$", token))
        
        def is_implicit_mul(self, token):
            # Check if we're in a situation like "2(" or "(3+4)(...)"
            if not self.tokens:
                return False
            
            prev_pos = max(0, self.pos - 1)
            prev_token = self.tokens[prev_pos] if prev_pos < len(self.tokens) else None
            curr_token = token
    
        def parse_implicit_mul(self):
            pass
    
    def is_implicit_mul_situation(tokens, pos):
        if pos <= 0 or pos >= len(tokens):
            return False
        
        prev_token = tokens[pos - 1]
        curr_token = tokens[pos]
        
        # Current token is '(' and previous is a number
        if curr_token == '(' and (prev_token.isdigit() or 
                                  (prev_token.startswith('-') and len(prev_token) > 1 and prev_token[1:].isdigit())):
            return True
        
        # Previous is ')' and current is '('
        if prev_token == ')' and curr_token == '(':
            return True
        
        return False
    
    # Process implicit multiplication in tokens
    i = 0
    new_tokens = []
    while i < len(tokens):
        token = tokens[i]
        if is_implicit_mul_situation(new_tokens, len(new_tokens)) and token == '(':
            new_tokens.append('*')
        new_tokens.append(token)
        i += 1
    
    tokens = new_tokens
    parser = Parser(tokens)
    result = parser.parse_expression()
    return result if not (result != result) else 0.0  # Return 0 for implicit mul errors
