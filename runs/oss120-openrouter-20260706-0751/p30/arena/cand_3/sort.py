def my_sort(xs):
    """Return a new list containing the elements of *xs* sorted in ascending order.

    The implementation is a classic top‑down merge‑sort which:
    * Handles all edge‑cases (empty list, single element, duplicated values,
      negative numbers, and arbitrarily large integers).
    * Preserves the multiset – each occurrence of a value in the input appears
      the same number of times in the output.
    * Runs in O(n log n) time and O(n) auxiliary space, making it fast for
      large arrays while using only the Python standard library.

    Args:
        xs (list): A list of comparable items.

    Returns:
        list: A new sorted list.
    """
    n = len(xs)
    if n <= 1:
        # Empty list or singleton – already sorted, but we must return a *new*
        # list object to satisfy the "new sorted list" contract.
        return list(xs)

    # Helper: merge two sorted sub‑lists into a new list.
    def _merge(left, right):
        merged = []
        i = j = 0
        len_left, len_right = len(left), len(right)
        while i < len_left and j < len_right:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        # One of the lists is exhausted – extend the remainder.
        if i < len_left:
            merged.extend(left[i:])
        if j < len_right:
            merged.extend(right[j:])
        return merged

    # Recursive top‑down merge sort.
    mid = n // 2
    left_sorted = my_sort(xs[:mid])
    right_sorted = my_sort(xs[mid:])
    return _merge(left_sorted, right_sorted)
