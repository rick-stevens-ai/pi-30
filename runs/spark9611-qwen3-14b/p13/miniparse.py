# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).
import re
def parse(s):
    s = s.strip()
    if s == 'null':
        return None
    elif s == 'true':
        return True
    elif s == 'false':
        return False
    elif s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    elif s.startswith('[') and s.endswith(']'):
        if s == '[]':
            return []
        remaining = s
        depth = 0
        for char in remaining:
            if char in '[{':
                depth += 1
            elif char in ']}':
                depth -= 1
            if char == ',' and depth == 0:
                elements.append(current)
                current = ''
            else:
                current += char
        if current:
            elements.append(current)
        return [parse(item.strip()) for item in elements]
    elif s.startswith('{') and s.endswith('}'):
        if s == '{}':
            return {}
        items = {}
        s = s[1:-1].strip()
        remaining = s[1:-1].strip()
        current = ''
        depth = 0
        for char in remaining:
            if char in '[{':
                depth += 1
            elif char in ']}':
                depth -= 1
            if char == ',' and depth == 0:
                key_val = current
                current = ''
                if ':' in key_val:
                    key_str, val_str = key_val.split(':', 1)
                    items[parse(key_str.strip())] = parse(val_str.strip())
                else:
                    raise ValueError(f"Invalid JSON: {key_val}")
            else:
                current += char
        if current:
            if ':' in current:
                key_str, val_str = current.split(':', 1)
                items[parse(key_str.strip())] = parse(val_str.strip())
            else:
                raise ValueError(f"Invalid JSON: {current}")
        return items
    elif re.fullmatch(r'-?\d*\.\d+', s):
        return float(s)
    elif re.fullmatch(r'-?\d+', s):
        return int(s)
        raise ValueError(f"Invalid JSON: {s}")
