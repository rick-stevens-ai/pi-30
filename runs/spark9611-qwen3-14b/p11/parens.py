# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def matches(opening, closing):
    return (opening == '(' and closing == ')') or (opening == '[' and closing == ']') or (opening == '{' and closing == '}')

def is_balanced(s):
    stack = []
    for ch in s:
        if ch in '({[':
            stack.append(ch)
        elif ch in ')}]':
            if not stack:
                return False
            top = stack.pop()
            if not matches(top, ch):
                return False
    return not stack
