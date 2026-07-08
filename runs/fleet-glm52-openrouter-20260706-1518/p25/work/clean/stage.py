# P25 clean stage: drop any element not convertible to float.
# Stdlib only.


def clean(rows) -> list[float]:
    """Drop any element not convertible to float (None, "", "x" -> dropped)."""
    out: list[float] = []
    for r in rows:
        try:
            out.append(float(r))
        except (TypeError, ValueError):
            continue
    return out
