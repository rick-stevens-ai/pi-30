# Fixed merge: sorts intervals, merges overlapping or touching intervals, and returns a list of tuples.
def merge(ivs):
    """Merge a list of intervals.

    Args:
        ivs (list[tuple[int, int]]): List of (start, end) intervals. Intervals may be
            unsorted and may overlap or touch. ``start`` should be <= ``end``.

    Returns:
        list[tuple[int, int]]: Merged, non‑overlapping intervals sorted by start.
    """
    if not ivs:
        return []
    # Sort intervals by their start coordinate (and end to guarantee deterministic order)
    sorted_ivs = sorted((a, b) for a, b in ivs)
    merged = []
    cur_start, cur_end = sorted_ivs[0]
    for a, b in sorted_ivs[1:]:
        # If intervals overlap or touch (a <= cur_end), extend the current interval
        if a <= cur_end:
            cur_end = max(cur_end, b)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = a, b
    merged.append((cur_start, cur_end))
    return merged
