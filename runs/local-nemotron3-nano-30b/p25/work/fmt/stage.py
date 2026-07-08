def fmt(d):
    pieces = []
    for key in sorted(d.keys()):
        pieces.append(f"{key}={d[key]}")
    return " ".join(pieces)