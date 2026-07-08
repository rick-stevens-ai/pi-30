"""Parse a JSON-subset string into Python values. No json module, no eval."""


def parse(s):  # noqa: D405,D401
    """Parse a JSON subset (null/true/false/int/float/string/array/object).

    Supports: nesting, whitespace between tokens and members, escaped quotes in strings.
    Raises ValueError on malformed input.
    """
    s = s.strip()
    if not s:
        return None

    pos = [0]  # mutable list so nested dispatch functions see updates
    value, _end_pos = _parse_value(s, pos)
    return value


def _is_ws(c):
    """Return True if character is whitespace."""
    return c in ' \t\n\r'


def _digit(ch):
    """Return True if ch is a digit character (0-9)."""
    return '0' <= ch <= '9'


_KEYW_MAP = {"null": None, "true": True, "false": False}


def _skip_ws(text, p):
    while p < len(text) and text[p] in (' ', '\t', '\n', '\r'):
        p += 1
    return p


def _parse_value(s, pos):
    """Parse top-level value. Returns (value, end_pos)."""
    s = s.strip()
    if not s:
        raise ValueError("empty input")
    _, new_end = _parse_prim(s)
    return new_end


def _parse_prim(src):
    """Try null/true/false first; then number; else expect '[' or '{'."""
    p = 0

    # Keywords: check null, true, false (in that order by keyword prefix safety)
    for kw in ("null", "true", "false"):
        klen = len(kw)
        if src[p:p + klen] == kw and (_is_ws(src[p]) or p + klen >= len(src)):
            return _KEYW_MAP[kw], p

    # String: starts with "
    if src[p] == '"':
        return _parse_string(src, p)

    # Array or object: '[' starts array, '{' starts object; else nothing parsed yet.
    saved_p = pos[0]  # but we don't have access to pos here — let's redesign
    _first_char = src[p]
    if _first_char in ('[', '{'):
        return _EMPTY_MARKER, p - 1

