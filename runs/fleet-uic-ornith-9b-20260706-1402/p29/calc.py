import re


def evaluate(expr):
    """Evaluate an arithmetic expression with +-*/, parentheses, and unary minus.

    Uses recursive-descent parsing — no eval() allowed.
    """
    tokens = _tokenize(expr)
    pos = [0]  # mutable index into token list
    result = _parse_expr(tokens, pos)
    if pos[0] < len(tokens):
        raise ValueError(f"Unexpected trailing token at position {pos[0]}")
    return result


# ---------- tokenizer ----------

def _tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        # number (integer or float, possibly with leading dot)
        if ch.isdigit() or (ch == "." and i + 1 < n and expr[i + 1].isdigit()):
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            tokens.append(("NUM", float(expr[i:j])))
            i = j
        elif ch in "+-*/()":
            tokens.append((ch,))
            i += 1
        else:
            raise ValueError(f"Unexpected character '{ch}' at position {i}")
    return tokens


# ---------- recursive-descent parser (precedence climbing) ----------

def _parse_expr(tokens, pos):       # + and - are lowest precedence
    val = _parse_term(tokens, pos)
    while pos[0] < len(tokens) and tokens[pos[0]][0] in "+-":
        op = tokens[pos[0]][0]
        pos[0] += 1
        rhs = _parse_term(tokens, pos)
        if op == "+":
            val += rhs
        else:
            val -= rhs
    return val


def _parse_term(tokens, pos):       # * and / higher than +/-
    val = _parse_unary(tokens, pos)
    while pos[0] < len(tokens) and tokens[pos[0]][0] in "*/":
        op = tokens[pos[0]][0]
        pos[0] += 1
        rhs = _parse_unary(tokens, pos)
        if op == "*":
            val *= rhs
        else:
            val /= rhs
    return val


def _parse_unary(tokens, pos):      # unary minus before a primary
    if (pos[0] < len(tokens) and tokens[pos[0]][0] == "-"):
        pos[0] += 1
        val = _parse_unary(tokens, pos)   # recursion for -- etc.
        return -val
    return _parse_primary(tokens, pos)


def _parse_primary(tokens, pos):    # number literal or parenthesised expr
    if pos[0] >= len(tokens):
        raise ValueError("Unexpected end of expression")
    tok_type = tokens[pos[0]][0]
    if tok_type == "NUM":
        val = tokens[pos[0]][1]
        pos[0] += 1
        return val
    if tok_type == "(":
        pos[0] += 1                     # consume '('
        val = _parse_expr(tokens, pos)
        if pos[0] >= len(tokens):
            raise ValueError("Missing ')'")
        if tokens[pos[0]][0] != ")":
            raise ValueError(f"Expected ')', got '{tokens[pos[0]][0]}'")
        pos[0] += 1                     # consume ')'
        return val
    raise ValueError(f"Unexpected token at position {pos[0]}: {tok_type}")
