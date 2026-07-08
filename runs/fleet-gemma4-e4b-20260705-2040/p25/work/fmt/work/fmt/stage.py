def fmt(d):
    """
    Formats a dictionary into a single line string 'k=v k=v ...' 
    with keys ALPHA-sorted, using only standard library components.
    """
    # Sort keys alphabetically
    sorted_keys = sorted(d.keys())
    
    # Format each key-value pair and join them with spaces
    parts = [f"{key}={d[key]}" for key in sorted_keys]
    return " ".join(parts)