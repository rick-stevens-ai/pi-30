# Fixed merge: sort intervals and combine overlapping or touching intervals.
# Returns a list of (start, end) tuples sorted by start.
def merge(ivs):
    if not ivs:
        return []
    # Sort intervals by start coordinate (and by end to stabilize)
    sorted_ivs = sorted(ivs, key=lambda x: (x[0], x[1]))
    merged = []
    for a, b in sorted_ivs:
        if not merged:
            merged.append([a, b])
        else:
            last_start, last_end = merged[-1]
            if a <= last_end:  # overlap or touch
                merged[-1][1] = max(last_end, b)
            else:
                merged.append([a, b])
    # Convert inner lists back to tuples for expected output format
    return [tuple(pair) for pair in merged]
