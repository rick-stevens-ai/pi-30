def my_sort(xs):
    """
    Return a new list containing all elements from xs in ascending order.
    Correctly handles empty lists, singletons, duplicates, negative numbers,
    and arbitrarily large integers. Preserves the multiset (i.e., no elements
    are lost or duplicated). Runs in O(n log n) time with O(n) auxiliary space.
    """
    n = len(xs)
    if n <= 1:
        # Return a shallow copy to ensure a new list is returned.
        return list(xs)
    
    mid = n // 2
    left = my_sort(xs[:mid])
    right = my_sort(xs[mid:])
    
    # Merge the two sorted halves.
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
    # Append any remaining elements.
    if i < len_left:
        merged.extend(left[i:])
    if j < len_right:
        merged.extend(right[j:])
    return merged