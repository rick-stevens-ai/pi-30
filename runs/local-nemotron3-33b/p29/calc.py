# P29 SEED: strictly left-to-right, no precedence, no parens, no unary minus.
#   "2+3*4"  -> 20 (wrong). Loop must implement proper precedence parsing.
# DO NOT use eval().
def evaluate( expr ):
    tokens  = _tokenize( expr )
    pos     = 0

    def peek():
        return tokens[ pos ] if pos < len( tokens ) else None

    def consume():
        nonlocal pos
        val = tokens[ pos ]
        pos += 1
        return val

    # ------- expression: addition / subtraction (lowest precedence) ----------
    def parse_expr():
        value  = parse_term()
        while peek() in ( '+', '-' ):
            op  = consume()
            rhs  = parse_term()
            if op == '+':
                value += rhs
            else:                     # '-'
                value -= rhs
        return value

    # ------- term: multiplication / division (mid precedence) -------------
    def parse_term():
        value  = parse_factor()
        while peek() in ( '*', '/' ):
            op  = consume()
            rhs  = parse_factor()
            if op == '*':
                value *= rhs
            else:                 # '/'
                value /= rhs      # true division; for integer-only you could use //.
        return value

    # ------- factor: parenthesized sub‑expression or numeric literal ----------
    def parse_factor():
        # optional unary sign
        sign  = 1.0
        if peek() == '+':
            consume()               # unary plus – does not affect value
        elif peek() == '-':
            sign  = -1.0
            consume()               # unary minus – apply later

        tok = peek()
        if tok == '(':
            consume()               # '('
            val_paren = parse_expr()   # full precedence inside parenthesis
            if peek() != ')':
                raise ValueError( "missing ')'" )
            consume()               # ')'
            return sign * val_paren
        else:
            # must be a number token
            num_str = consume()
            try:
                number = float( num_str )
            except Exception as e:
                raise ValueError( f"could not convert string '{ num_str }'") from e
            return sign * number

    # ------------------------- overall entry point ---------------------------
    result  = parse_expr()

    if pos != len( tokens ):
        raise ValueError( "invalid expression: extra tokens after parsing" )

    return result


def _tokenize( s ):
    """Return a list of tokens: numbers (as strings), operators, and parentheses; whitespace removed."""
    import re
    # match numbers (integer or decimal), each operator as separate token,
    # and '(' or ')'.  any surrounding whitespace is ignored.
    pattern = r'\d+\.?\d*|[+\-*/()]|\s+'
    raw = re.findall( pattern, s.replace( "   ", " " ) )
    # filter out pure whitespace tokens
    return [ tok for tok in raw if not tok.strip() == '' ]