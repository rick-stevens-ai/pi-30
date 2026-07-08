# fmt stage implementation

def fmt(d):
    """Format a dictionary into a single line string.

    The output consists of key=value pairs separated by a single space,
    with the keys sorted alphabetically (lexicographically).
    Values are converted to their string representation using ``str``.

    Args:
        d (dict): Mapping of keys to values.

    Returns:
        str: Formatted string.
    """
    # Ensure we work with a dict; let errors surface if not.
    # Sort the keys alphabetically and build ``k=v`` strings.
    parts = []
    for key in sorted(d.keys()):
        parts.append(f"{key}={d[key]}")
    return " ".join(parts)
