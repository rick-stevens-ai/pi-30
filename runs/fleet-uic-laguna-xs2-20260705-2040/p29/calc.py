# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
# "2+3*4" -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().

import re

def evaluate(expr):
    expr = expr.replace(" ", "")
    
    # Tokenize: numbers (no leading sign), operators, and parens
    # Numbers: digits with optional decimal point
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c in '0123456789.':
            # Parse number
            j = i
            if c == '.':
                j += 1
                while j < len(expr) and expr[j] in '0123456789':
                    j += 1
            else:
                j += 1
                while j < len(expr) and expr[j] in '0123456789.':
                    j += 1
            tokens.append(expr[i:j])
            i = j
        elif c in '+-*/()':
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"Invalid character: {c}")
    
    pos = [0]
    
    def parse_expr():
        """expr ::= term (('+' | '-') term)*"""
        result = parse_term()
        while pos[0] < len(tokens) and tokens[pos[0]] in ('+', '-'):
            op = tokens[pos[0]]
            pos[0] += 1
            right = parse_term()
            if op == '+':
                result += right
            else:
                result -= right
        return result
    
    def parse_term():
        """term ::= factor (('*' | '/') factor)*"""
        result = parse_factor()
        while pos[0] < len(tokens) and tokens[pos[0]] in ('*', '/'):
            op = tokens[pos[0]]
            pos[0] += 1
            right = parse_factor()
            if op == '*':
                result *= right
            else:
                result /= right
        return result
    
    def parse_factor():
        """factor ::= number | '-' factor | '(' expr ')'"""
        if pos[0] >= len(tokens):
            raise ValueError("Unexpected end of expression")
        
        if tokens[pos[0]] == '(':
            pos[0] += 1
            result = parse_expr()
            if pos[0] >= len(tokens) or tokens[pos[0]] != ')':
                raise ValueError("Missing closing parenthesis")
            pos[0] += 1
            return result
        
        if tokens[pos[0]] == '-':
            pos[0] += 1
            return -parse_factor()
        
        # number
        num_str = tokens[pos[0]]
        pos[0] += 1
        return float(num_str)
    
    result = parse_expr()
    if pos[0] != len(tokens):
        raise ValueError("Unexpected tokens at end of expression")
    return result