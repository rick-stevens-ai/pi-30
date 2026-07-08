def is_balanced(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opens = set(pairs.values())
    
    for ch in s:
        if ch in opens:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack