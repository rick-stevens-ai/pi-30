# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def is_balanced(s):
    stack = []
    mapping = {"(": ")", "[": "]", "{": "}"}
    for ch in s:
        if ch in mapping:
            stack.append(ch)
        elif ch in mapping.values():
            if not stack or ch != mapping[stack.pop()]:
                return False
    return not stack
