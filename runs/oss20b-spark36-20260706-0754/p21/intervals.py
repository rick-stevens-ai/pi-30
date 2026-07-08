# P21 SEED: merges only consecutive-in-INPUT intervals, no sorting. Wrong when
# input is unsorted or has non-adjacent overlaps.
def merge(ivs):
    """
    Merge a list of intervals into non‑overlapping, contiguous intervals.
    
    Parameters
    ----------
    ivs : list[tuple[int,int]] | list[list[int,int]]
        Input intervals. The function does not modify the input list.
    
    Returns
    -------
    list[tuple[int,int]]
        Sorted and merged intervals, with overlapping or touching intervals combined.
    """
    if not ivs:
        return []

    # Sort by start point (and end for stability)
    sorted_ivs = sorted(ivs, key=lambda x: (x[0], x[1]))
    merged: list[tuple[int, int]] = []
    cur_start, cur_end = sorted_ivs[0]

    for a, b in sorted_ivs[1:]:
        if a <= cur_end:
            # Overlap or touch – extend the current interval.
            cur_end = max(cur_end, b)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = a, b
    merged.append((cur_start, cur_end))
    return merged
