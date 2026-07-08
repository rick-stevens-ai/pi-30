"""Merge a list of intervals.

The function accepts an iterable of ``(start, end)`` tuples (or any
two‑item sequence) and returns a list of **merged, non‑overlapping**
intervals sorted by their start coordinate.

Two intervals are merged when they overlap **or touch** – i.e. when the
start of the later interval is less than or equal to the end of the
current merged interval.

The original implementation only merged consecutive intervals in the
input order and returned a list of mutable ``list`` objects.  This broke
for unsorted inputs and produced the wrong type.  The corrected version
first sorts the intervals, then merges them, and finally returns a list
of immutable ``tuple`` objects as expected by the tests.
"""

def merge(ivs):
    """Return a sorted list of merged intervals.

    Parameters
    ----------
    ivs : iterable of tuple(int, int)
        Intervals to be merged.  Each interval is a ``(start, end)`` pair
        where ``start`` <= ``end``.

    Returns
    -------
    list[tuple[int, int]]
        Merged, non‑overlapping intervals sorted by ``start``.
    """
    # Convert to list to allow sorting and multiple passes.
    ivs = list(ivs)
    if not ivs:
        return []

    # Ensure intervals are sorted by their start coordinate.
    ivs.sort(key=lambda x: x[0])

    merged = []
    cur_start, cur_end = ivs[0]
    for start, end in ivs[1:]:
        if start <= cur_end:  # Overlap or touch
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end
    # Append the final interval.
    merged.append((cur_start, cur_end))
    return merged

