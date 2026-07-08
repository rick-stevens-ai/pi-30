def parse(s):
    s = s.strip()
    if s == 'null':
        return None
    elif s.lower() in ('true', 'false'):
        return s.lower() == 'true'
    elif isinstance(s, str) and (s.startswith('"') or s.endswith('"')):
        # Handle string - remove quotes and escape characters if necessary
        return ''.join(chr(ord(c)) for c in s[1:-1])
    elif s.isdigit() or ('.' in s and all(c.isdigit() or c == '.' for c in s)):
        # Handle number (integer or float)
        try:
            return int(s)
        except ValueError:
            return float(s)
    elif s.startswith('[') or s.startswith('{'):
        # Handle array or object - implement recursive parsing
        pass
