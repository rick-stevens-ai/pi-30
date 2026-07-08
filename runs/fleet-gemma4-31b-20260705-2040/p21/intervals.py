def merge(ivs):
    if not ivs:
        return []
    sorted_ivs = sorted(ivs)
    out = []
    curr_start, curr_end = sorted_ivs[0]
    for next_start, next_end in sorted_ivs[1:]:
        if next_start <= curr_end:
            curr_end = max(curr_end, next_end)
        else:
            out.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end
    out.append((curr_start, curr_end))
    return out
