"""fmt stage: format an aggregation dict into a single sorted line.

fmt(d) -> "k=v k=v ..." with keys in alphabetical order.
"""


def fmt(d):
    """Format *d* into a single line of ``key=value`` pairs.

    Keys are emitted in alphabetical order, space-separated, so the
    output is deterministic and easy to compare.  Values use their
    natural string representation (``int`` stays integral, ``float``
    keeps its ``.0`` suffix).
    """
    return " ".join(f"{k}={d[k]}" for k in sorted(d))