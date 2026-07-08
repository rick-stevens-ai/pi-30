def is_balanced(s):
    stack = []
    matching = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    for c in s:
        if c in matching.values():
            print('Pushing opening bracket:', c)
            stack.append(c)
        elif c in matching.keys():
            if not stack or stack.pop() != matching[c]:
                print(f'Mismatch detected: {c} does not match expected {matching[c]}')
                return False
    return len(stack) == 0