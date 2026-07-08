# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.

def is_balanced(s: str) -> bool:
    """Return ``True`` if *s* contains balanced parentheses, brackets and braces.

    The function ignores any characters that are not one of ``(``, ``)``, ``[``,
    ``]``, ``{`` or ``}``. It uses a stack to ensure that closing characters match
    the most‑recently seen opening character.
    """
    # Mapping from closing bracket to its corresponding opening bracket
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())
    stack: list[str] = []

    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        # ignore all other characters
    return not stack

