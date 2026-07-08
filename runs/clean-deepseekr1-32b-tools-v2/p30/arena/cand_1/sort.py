# Sort implementation with built-in sorted for performance and correctness

def my_sort(xs):
    # Validate input is a sequence/iterable
    if isinstance(xs, (str, bytes)):
        raise TypeError('Input must be list-like or tuple-like')
    try:
        iter(xs)
    except TypeError:
        raise TypeError('Input is not an iterable')
    # Early return for empty
    if len(xs) == 0:
        return xs
    # Ensure we have a consistent type
    return sorted(list(xs))