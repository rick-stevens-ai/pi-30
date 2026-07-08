# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def is_balanced(s):
    """Check if brackets in *s* are balanced.

    Supports round parentheses ``()``, square brackets ``[]`` and curly braces ``{}``.
    All other characters are ignored. The function uses a stack to ensure that each
    closing bracket matches the most recent unmatched opening bracket.
    """
    stack = []
    opening = "({["
    matching = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in matching:
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()
    return not stack
