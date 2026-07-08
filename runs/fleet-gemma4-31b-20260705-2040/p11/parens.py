# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())
    closing = set(pairs.keys())

    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif ch in closing:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
