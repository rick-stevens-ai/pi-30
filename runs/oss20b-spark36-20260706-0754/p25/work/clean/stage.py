# clean stage: filter rows that can be converted to float

def clean(rows):
    """Return a list of floats extracted from *rows*.

    Non‑convertible values (``None``, empty string, and any value that raises
    ``ValueError``/``TypeError`` when passed to :func:`float`) are dropped.
    """
    out = []
    for r in rows:
        try:
            # Skip ``None`` explicitly – it would raise TypeError which we handle below
            if r is None:
                continue
            f = float(r)
            out.append(f)
        except Exception:
            continue
    return out
