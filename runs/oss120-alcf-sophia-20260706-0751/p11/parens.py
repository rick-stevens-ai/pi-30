# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.

def is_balanced(s):
    """Check if a string contains balanced brackets.

    Supports parentheses ``()``, square brackets ``[]`` and curly braces ``{}``.
    All other characters are ignored. The function returns ``True`` when every
    opening bracket is closed by the corresponding closing bracket in the correct
    order, otherwise ``False``.
    """
    stack = []
    opening = "([{"
    matching = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in matching:
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()
        # ignore any other characters
    return not stack
