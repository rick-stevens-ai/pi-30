"""fmt stage implementation.

According to the plan, this stage receives a dictionary (the output of the `agg` stage)
and should produce a single string where each key/value pair is formatted as
`k=v`.  The pairs must be ordered by key in alphabetical order and separated by
a single space.

Only the Python standard library is used.
"""

def fmt(d):
    """Return a single‑line string representation of a dict.

    Args:
        d (dict): Mapping of keys to values, typically numeric statistics.

    Returns:
        str: Space‑separated ``k=v`` pairs with keys sorted alphabetically.
    """
    # Sort the items by key (alphabetically) and format each as "k=v".
    # ``str`` is sufficient for values – the ``agg`` stage already produces
    # appropriate numeric types.
    return " ".join(f"{k}={v}" for k, v in sorted(d.items()))

__all__ = ["fmt"]
