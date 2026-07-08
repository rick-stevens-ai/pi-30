# fmt stage: format statistics dictionary into a single sorted string

def fmt(d):
    """Return a one‑line representation of *d*.

    The line contains ``key=value`` pairs sorted alphabetically by key and
    separated by spaces.  All numeric values are converted to ``float`` first so
    that integers appear with a decimal point (e.g., ``1`` → ``1.0``).  This
    matches the expected output in :mod:`verify`.
    """
    # Sort keys alphabetically and join into the requested format.
    return " ".join(f"{k}={float(d[k])}" for k in sorted(d))
