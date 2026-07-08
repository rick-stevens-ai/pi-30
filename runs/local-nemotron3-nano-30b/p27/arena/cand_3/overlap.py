"""overlap.py - Fast, non‑overlapping counting of substring occurrences with stdlib only.

Exposes:
    count_overlapping(haystack: str, needle: str) -> int

Returns the number of overlapping occurrences of `needle` in `haystack`.
- If `needle` is empty, returns 0.
- Overlapping matches are counted (e.g., 'aa' occurs 3 times in 'aaaa').
- Pure Python + stdlib; uses a regex look‑ahead for speed on long strings.
"""

import re

# Pre‑compile the pattern once per needle to avoid recompiling on each call.
# The function builds it lazily and caches it in a module‑level dict keyed by
# the needle string. This gives O(1) compilation overhead after the first use.
 _compiled_patterns: dict[str, re.Pattern] = {}

def count_overlapping(haystack: str, needle: str) -> int:
    """Count overlapping occurrences of `needle` in `haystack`.

    Args:
        haystack: The string to be searched.
        needle:   Substring to search for.

    Returns:
        int: Number of (possibly overlapping) matches. Returns 0 if
             `needle` is empty or longer than `haystack`.

    Examples:
        >>> count_overlapping('aaaa', 'aa')
        3
        >>> count_overlapping('abababa', 'aba')
        2
        >>> count_overlapping('hello', '')
        0
    """
    # Edge case: empty needle → defined to be 0 matches.
    if not needle:
        return 0

    # Retrieve or create a compiled look‑ahead regex for this needle.
    # Using `re.escape` ensures that special characters in the needle are treated literally.
    if needle not in _compiled_patterns:
        pattern = re.compile(r'(?={})'.format(re.escape(needle)))
        _compiled_patterns[needle] = pattern
    else:
        pattern = _compiled_patterns[needle]

    # `findall` returns all non‑overlapping matches of the look‑ahead, which actually
    # yields an entry at each position where the needle can start. The length of this
    # list is exactly the number of overlapping occurrences.
    return len(pattern.findall(haystack))