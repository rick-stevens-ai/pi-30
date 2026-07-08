# P11 fixed to handle (), [], {} via a stack.
def is_balanced(s):
    STACK = []
    MATCH = {')': '(', ']': '[', '}': '{'}
    OPEN = {'(', '[', '{'}

    for ch in s:
        if ch in OPEN:
            STACK.append(ch)
        elif ch in MATCH:
            # Closing bracket found — check it matches the most recent open
            top = STACK.pop() if STACK else None  # noqa (top is str | None per pyright analysis)
            if top != MATCH[ch]:
                return False
    
    # True only when everything is properly paired and closed
    return len(STACK) == 0
