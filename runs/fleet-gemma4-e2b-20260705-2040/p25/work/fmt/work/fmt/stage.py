def fmt(d: dict) -> str:
    """
    Formats the aggregated data dictionary into a single line string 
    with alphabetically sorted keys in the format 'k=v k=v ...'.
    
    Args:
        d: A dictionary containing aggregated statistics (e.g., {'count': 10, 'sum': 50.5}).

    Returns:
        A formatted string like "key1=value1 key2=value2 ...".
    """
    # Get keys and sort them alphabetically
    sorted_keys = sorted(d.keys())
    
    # Format each key-value pair
    parts = []
    for key in sorted_keys:
        # Ensure values are converted to strings for formatting
        value = str(d[key])
        parts.append(f"{key}={value}")
        
    # Join them with a space
    return " ".join(parts)

if __name__ == '__main__':
    # Example usage
    sample_data = {
        'min': 10.5,
        'max': 99.9,
        'count': 100,
        'sum': 500.5
    }
    result = fmt(sample_data)
    print(f"Input: {sample_data}")
    print(f"Output: {result}")

    # Expected output check (keys sorted: count, max, min, sum)
    # Expected: count=100 max=99.9 min=10.5 sum=500.5
