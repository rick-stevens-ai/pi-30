# P21 SEED: merges only consecutive-in-INPUT intervals, no sorting. Wrong when
# input is unsorted or has non-adjacent overlaps.
def merge(ivs):
    if not ivs:
        return []
    s = sorted(tuple(x) for x in ivs)
    out = [list(s[0])]
    for a, b in s[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
