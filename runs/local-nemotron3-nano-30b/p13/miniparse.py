# P13 Parser for JSON subset without using json or eval.
# Supports null/true/false/int/float/string/array/object, nesting, whitespace.

import sys

def parse(s):
    # Internal helper that tracks current position
    def parse_value(i):
        # Skip leading whitespace
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s):
            raise ValueError("unexpected end of input")

        c = s[i]

        # Object {'key': value, ...}
        if c == '{':
            return parse_object(i)
        # Array [...] 
        elif c == '[':
            return parse_array(i)
        # String "..."
        elif c == '"' or c == '\' and i+1 < len(s) and s[i+1] == '"':  # handle escaped opening quote? not needed
            return parse_string(i)
        # Number (int or float)
        elif c in '-0123456789.':
            return parse_number(i)
        # Literals true / false / null
        elif c == 't' and s.startswith('true', i):
            return True, i + 4
        elif c == 'f' and s.startswith('false', i):
            return False, i + 5
        elif c == 'n' and s.startswith('null', i):
            return None, i + 4
        else:
            raise ValueError(f"unexpected character {c} at position {i}")

    # ---- Object parsing ----
    def parse_object(i_start):
        i = i_start + 1  # skip '{'
        obj = {}
        while True:
            # Skip whitespace after '{' or ','
            while i < len(s) and s[i].isspace():
                i += 1
            if i >= len(s):
                raise ValueError("unterminated object literal")
            if s[i] == '}':
                return obj, i + 1
            # Parse key (must be a string)
            if s[i] != '"':
                raise ValueError("object key must be a quoted string")
            key, i = parse_string(i)
            # Skip colon and whitespace
            while i < len(s) and s[i].isspace():
                i += 1
            if i >= len(s) or s[i] != ':':
                raise ValueError("expected ':' after object key")
            i += 1  # skip ':'
            # Parse value
            val, i = parse_value(i)
            obj[key] = val
            # Skip trailing comma or whitespace before next key or closing brace
            while i < len(s) and s[i].isspace():
                i += 1
            if i >= len(s):
                raise ValueError("unterminated object literal")
            if s[i] == ',':
                i += 1
                continue
            elif s[i] == '}':
                return obj, i + 1
        # unreachable

    # ---- Array parsing ----
    def parse_array(i_start):
        i = i_start + 1  # skip '['
        arr = []
        while True:
            # Skip whitespace after '[' or ','
            while i < len(s) and s[i].isspace():
                i += 1
            if i >= len(s):
                raise ValueError("unterminated array literal")
            if s[i] == ']':
                return arr, i + 1
            # Parse element
            elem, i = parse_value(i)
            arr.append(elem)
            # Skip trailing comma or closing bracket
            while i < len(s) and s[i].isspace():
                i += 1
            if i >= len(s):
                raise ValueError("unterminated array literal")
            if s[i] == ',':
                i += 1
                continue
            elif s[i] == ']':
                return arr, i + 1
        # unreachable

    # ---- String parsing ----
    def parse_string(i_start):
        i = i_start + 1  # skip opening quote
        chars = []
        while True:
            if i >= len(s):
                raise ValueError("unterminated string literal")
            ch = s[i]
            if ch == '"':
                return "".join(chars), i + 1
            elif ch == '\\':
                i += 1
                if i >= len(s):
                    raise ValueError("unescaped backslash at end of string")
                esc = s[i]
                unescaped = {
                    '"': '"',
                    '\\': '\\',
                    '/': '/',
                    'b': '\x08',  # backspace
                    'f': '\x0C',  # form feed
                    'n': '\x0A',  # newline
                    'r': '\x0D',  # carriage return
                    't': '\x09',  # tab
                }.get(esc)
                if unescaped is None:
                    # Simple pass-through for other escapes (e.g. "u" handling could be added)
                    unescaped = esc
                chars.append(unescaped)
            else:
                chars.append(ch)
            i += 1
        # unreachable

    # ---- Number parsing ----
    def parse_number(i_start):
        i = i_start
        start_i = i
        c = s[i]
        if c == '-':
            i += 1
        # Digits before dot or exponent
        while i < len(s) and s[i].isdigit():
            i += 1
        # Optional fractional part
        if i < len(s) and s[i] == '.':
            i += 1
            has_digit = False
            while i < len(s) and s[i].isdigit():
                i += 1
                has_digit = True
            if not has_digit:
                raise ValueError("malformed fractional part in number")
        # Optional exponent part
        exp_start = i
        if i < len(s) and s[i] in 'eE':
            i += 1
            if i >= len(s):
                raise ValueError("exponent without digits")
            if s[i] in '+-':
                i += 1
            exp_digits = 0
            while i < len(s) and s[i].isdigit():
                i += 1
                exp_digits += 1
            if exp_digits == 0:
                raise ValueError("exponent has no digits")
        # Extract numeric substring
        num_str = s[start_i:i]
        if '.' in num_str or 'e' in num_str.lower():
            try:
                return float(num_str)
            except ValueError as exc:
                raise ValueError(f"cannot parse number {num_str}") from exc
        else:
            try:
                return int(num_str)
            except ValueError as exc:
                raise ValueError(f"cannot parse integer {num_str}") from exc

    # Begin parsing from the top level
    result, next_i = parse_value(0)
    # Allow trailing whitespace but no extra non-whitespace characters
    while next_i < len(s) and s[next_i].isspace():
        next_i += 1
    if next_i != len(s):
        raise ValueError(f"trailing characters after parse position {next_i}")
    return result

