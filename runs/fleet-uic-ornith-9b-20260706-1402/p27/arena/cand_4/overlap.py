def count_overlapping(haystack: str, needle: str) -> int:
    """Count overlapping occurrences of *needle* in *haystack*.

    An empty needle always returns 0.
    Uses a sliding-window approach over C-level ``str.find`` so that each
    occurrence is located by the native search engine rather than re-scanning
    Python-character-by-character.
    """
    if not needle or len(needle) > len(haystack):
        return 0

    n = len(haystack)
    m = len(needle)

    # --- fast path: short needles ------------------------------------------
    # For small *m* the find loop is dominated by a handful of C calls and
    # catches every overlapping hit in near-linear time.
    if m <= 5:
        count = 0
        start = 0
        while True:
            idx = haystack.find(needle, start)
            if idx == -1:
                break
            count += 1
            start = idx + 1          # slide by one → overlaps detected
        return count

    # --- general path ------------------------------------------------------
    # For longer needles we still use ``find`` to skip non-matching regions,
    # but after each hit we manually scan the next *m-1* positions (pure
    # Python slices) to pick up any overlapping matches that str.find()
    # would otherwise skip because its C engine advances past them.
    count = 0
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            break

        count += 1
        # Scan ahead for overlapping matches; each one is counted and we
        # continue scanning from the next position until no more fit.
        j = 1
        while idx + j < n - m + 1:
            if haystack[idx + j : idx + j + m] == needle:
                count += 1
                j += 1
            else:
                break

        start = idx + j              # advance past all clusters found here

    return count
