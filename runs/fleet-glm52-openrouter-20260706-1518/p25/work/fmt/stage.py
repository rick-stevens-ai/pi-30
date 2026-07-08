# P25 fmt stage: fmt(d) -> single line "k=v k=v ..." with keys alpha-sorted.
def fmt(d):
    return " ".join(f"{k}={d[k]}" for k in sorted(d))
