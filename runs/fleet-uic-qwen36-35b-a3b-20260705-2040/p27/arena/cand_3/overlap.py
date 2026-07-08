"""Candidate #3: regex positive-lookahead — never consumes characters, so every
position where the needle starts is found, naturally giving overlapping matches.
Fast because the matching runs in C inside the stdlib ``re`` module."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:                     # empty needle → 0 by contract
        return 0
    return len(re.findall(f"(?={re.escape(needle)})", haystack))
