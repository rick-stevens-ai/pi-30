# P11 SEED: only handles round parens, ignores []{}, and uses a counter (so it
# accepts "([)]"). Loop must use a stack and all three bracket types.
def is_balanced(s):
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in mapping.values():  # Opening characters: '(', '[', '{'
            stack.append(char)
        elif char in mapping.keys():  # Closing characters: ')', ']', '}'
            if not stack:
                return False # No corresponding opening bracket found
            top_element = stack.pop()
            if top_element != mapping[char]:
                return False # Mismatched brackets
    return not stack
