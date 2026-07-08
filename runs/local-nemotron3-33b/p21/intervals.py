# P21 SEED: sort intervals first, then merge any overlapping or touching intervals.
def merge(ivs):
    if not ivs:
        return []
    # sort intervals by start coordinate
    sorted_ivs = sorted(ivs, key=lambda x: x[0])
    out = [list(sorted_ivs[0])]
    for a, b in sorted_ivs[1:]:
        if a <= out[-1][1]:  # overlapping (includes touching)
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out