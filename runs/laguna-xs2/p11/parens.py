def is_balanced(s):
    """Validate parens, brackets, braces via stack, ignoring other chars."""
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    opening = set('([{"')
    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in mapping:
            if not stack or stack[-1] != mapping[ch]:
                return False
            stack.pop()
    return not stack
