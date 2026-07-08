def is_balanced(s):
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    openers = set(["(", "[", "{"])
    closers = set([")", "]", "}"])

    for char in s:
        if char in openers:
            stack.append(char)
        elif char in closers:
            if not stack:
                return False
            top_element = stack.pop()
            if mapping[char] != top_element:
                return False

    return not stack
