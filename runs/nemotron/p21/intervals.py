def merge(ivs):
    if not ivs:
        return []
    # Sort intervals by start value
    sorted_ivs = sorted(ivs, key=lambda x: x[0])
    out = [list(sorted_ivs[0])]
    for a, b in sorted_ivs[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
