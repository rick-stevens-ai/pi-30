# P21 SEED: merges only consecutive-in-INPUT intervals, no sorting. Wrong when
# input is unsorted or has non-adjacent overlaps.
def merge(ivs):
    if not ivs:
        return []
    # Sort intervals by start
    sorted_intervals = sorted(ivs, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]
    for a, b in sorted_intervals[1:]:
        if a <= merged[-1][1]:  # overlapping or touching
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [tuple(m) for m in merged]
