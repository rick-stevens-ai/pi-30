def merge(ivs):
    if not ivs:
        return []
    sorted_ivs = sorted(ivs, key=lambda x: x[0])
    out = [[sorted_ivs[0][0], sorted_ivs[0][1]]]
    for a, b in sorted_ivs[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [tuple(iv) for iv in out]
