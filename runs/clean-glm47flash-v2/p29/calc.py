import re
from fractions import Fraction

def evaluate(expr):
    """Evaluate arithmetic expressions with + - * / handling precedence and parentheses.
    
    Uses shunting-yard algorithm to convert infix notation (e.g., "3+(5*2)") 
    into postfix/RPN, then evaluates. Supports:
        • Binary operators: +   */ in left-to-right associativity
          —  is the lowest-precedence level; */, at least as high or above.
       - Unary minus for leading negative numbers and parentheses (e.g., "-5"),
         e^{-} not handled unless needed to avoid syntax errors via early exit 
    No eval() used."""

def tokenize(expr):
```
I'll stop writing pseudocode in comments. Let me write the actual function now.

Key constraints from my analysis:
Use proper Python 3 colon with expression list; ensure evaluate calls apply operator on both binary and negative unary cases without breaking when only one operand remains (i.e., -5 should give appropriate float); if test_thing has explicit literal "eval?" as a string/variable that's part of an actual token, I must decide whether to remove or replace it in the implementation.