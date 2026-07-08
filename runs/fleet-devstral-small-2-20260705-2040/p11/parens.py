def is_balanced(s):
    stack = []
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    opening_brackets = set(bracket_pairs.values())
    closing_brackets = set(bracket_pairs.keys())
    
    for ch in s:
        if ch in opening_brackets:
            stack.append(ch)
        elif ch in closing_brackets:
            if not stack or stack[-1] != bracket_pairs[ch]:
                return False
            stack.pop()
    
    return len(stack) == 0
