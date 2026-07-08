"""Count overlapping occurrences of *needle* in *haystack*.

Candidate #2 — a distinct angle: leverage str.find() (C-level search) with
a one-step restart loop instead of the usual naive slice-generate or regex
approaches.  When no match exists at a position, find() does big jumps in C;
only on successive matches do we step forward by one to capture overlaps.

Edge case: empty needle returns 0 immediately."""


def count_overlapping(haystack: str, needle: str) -> int:
    if not needle:                      # empty needle → 0 (spec contract)
        return 0
    count = 0
    start = 0
    while True:
        pos = haystack.find(needle, start)   # C-optimized search
        if pos == -1:                            # exhausted — done
            break
        count += 1
        start = pos + 1                          # advance by ONE for overlap
    return count
