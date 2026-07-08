def merge(ivs):
    if not ivs:
        return []
    ivs.sort(key=lambda x: x[0])
    out = [list(ivs[0])]
    for a, b in ivs[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
