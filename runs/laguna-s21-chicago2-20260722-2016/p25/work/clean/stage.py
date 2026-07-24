"""Clean stage: drop any element not convertible to float."""


def clean(rows):
    """Return list[float] of elements in *rows* convertible to float.

    Elements that raise ValueError or TypeError under float() — such as
    None, "", "x" — are silently dropped.
    """
    out = []
    for r in rows:
        try:
            out.append(float(r))
        except (ValueError, TypeError):
            pass
    return out