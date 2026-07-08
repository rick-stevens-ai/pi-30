# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
def parse(s):
    s = s.strip()
    if not s:
        raise ValueError("Empty input")

    # Handle string literals (e.g., "hi")
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]

    # Handle null, true, false, numbers (int/float)
    if s == "null":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    try:
        # Try parsing as int first
        return int(s)
    except ValueError:
        try:
            # Try parsing as float
            return float(s)
        except ValueError:
            pass

    # Handle arrays (e.g., [1, 2])
    if s.startswith('[') and s.endswith(']'):
        content = s[1:-1].strip()
        if not content:
            return []
        
        elements = []
        balance = 0
        start_index = 0
        for i, char in enumerate(content):
            if char in ('[', '{'):
                balance += 1
            elif char in (']', '}'):
                balance -= 1
            elif char == ',' and balance == 0:
                elements.append(content[start_index:i].strip())
                start_index = i + 1
        
        # Add the last element
        if start_index <= len(content):
            elements.append(content[start_index:].strip())

        # Recursively parse each element
        return [parse(item) for item in elements if item]

    # Handle objects (e.g., {"a": 1}) - This is the hardest part without eval/json.
    if s.startswith('{') and s.endswith('}'):
        content = s[1:-1].strip()
        if not content:
            return {}
        
        result = {}
        balance = 0
        start_index = 0
        i = 0
        while i < len(content):
            char = content[i]
            if char in ('[', '{'):
                balance += 1
            elif char in (']', '}'):
                balance -= 1
            elif char == ',' and balance == 0:
                part = content[start_index:i].strip()
                if part:
                    if ':' in part:
                        key_part, value_part = part.split(':', 1)
                        key = key_part.strip()
                        # Strip quotes from keys to get Python identifiers
                        if key.startswith('"') and key.endswith('"'):
                            key = key[1:-1]
                        value_str = value_part.strip()
                        result[key] = parse(value_str)
                start_index = i + 1
            i += 1
        
        # Add the last part
        part = content[start_index:].strip()
        if part:
            if ':' in part:
                key_part, value_part = part.split(':', 1)
                key = key_part.strip()
                if key.startswith('"') and key.endswith('"'):
                    key = key[1:-1]
                value_str = value_part.strip()
                result[key] = parse(value_str)

        return result

    raise ValueError(f"Could not parse input: {s}")