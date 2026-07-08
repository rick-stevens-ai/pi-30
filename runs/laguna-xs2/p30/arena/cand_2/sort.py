"""Sort implementation: iterative bottom-up merge sort.

O(n log n) time, O(n) extra space. Stable, handles all types
comparable by < (ints, big ints, negatives, dupes, etc.).
"""


def my_sort(xs):
    """Return a new sorted list (ascending) from input list xs.

    Args:
        xs: List of comparable elements (ints, big ints, etc.)

    Returns:
        New list with same elements in ascending order.
    """
    if not xs or len(xs) < 2:
        return list(xs)

    # Iterative bottom-up merge sort
    # Avoids recursion limit issues, stable, O(n log n)
    n = len(xs)
    result = list(xs)
    aux = [None] * n

    # Start with runs of size 1, double each pass
    run_size = 1
    while run_size < n:
        for start in range(0, n, 2 * run_size):
            mid = min(start + run_size, n)
            end = min(start + 2 * run_size, n)

            # Merge result[start:mid] and result[mid:end] into aux[start:end]
            i, j, k = start, mid, start
            left_end = mid

            while i < left_end and j < end:
                if result[i] <= result[j]:
                    aux[k] = result[i]
                    i += 1
                else:
                    aux[k] = result[j]
                    j += 1
                k += 1

            # Copy remaining left elements
            while i < left_end:
                aux[k] = result[i]
                i += 1
                k += 1

            # Copy remaining right elements
            while j < end:
                aux[k] = result[j]
                j += 1
                k += 1

        # Swap result and aux
        result, aux = aux, result
        run_size *= 2

    return result