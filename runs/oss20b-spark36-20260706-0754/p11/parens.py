# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def is_balanced(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    opening = set(mapping.values())
    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in mapping:
            if not stack or stack.pop() != mapping[ch]:
                return False
    return not stack
