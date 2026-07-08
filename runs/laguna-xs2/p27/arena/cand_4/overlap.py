"""Count overlapping occurrences of a substring in a string."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of needle in haystack.

    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('abababa', 'aba')
    3
    >>> count_overlapping('hello', '')
    0
    >>> count_overlapping('', 'a')
    0
    """
    if not needle:
        return 0

    # Use lookahead to find all positions where needle could start.
    # This naturally handles overlapping matches.
    pattern = f'(?=({re.escape(needle)}))'
    return len(re.findall(pattern, haystack))


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        print(count_overlapping(sys.argv[1], sys.argv[2]))
    else:
        print('Usage: python overlap.py <haystack> <needle>')
        sys.exit(1)