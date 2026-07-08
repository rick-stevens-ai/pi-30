# clean stage implementation
# According to ../../PLAN.md, this module provides a single function:
#   clean(rows) -> list[float]
# It should drop any element that cannot be converted to a float, such as
# None, empty strings, or arbitrary non‑numeric values.
# Only the standard library may be used.

def clean(rows):
    """Return a list of floats extracted from *rows*.

    Elements that raise ``TypeError`` or ``ValueError`` when passed to ``float``
    are ignored. The order of the remaining elements is preserved.
    """
    cleaned = []
    for item in rows:
        try:
            cleaned.append(float(item))
        except (TypeError, ValueError):
            # Skip items that cannot be interpreted as a float
            continue
    return cleaned
