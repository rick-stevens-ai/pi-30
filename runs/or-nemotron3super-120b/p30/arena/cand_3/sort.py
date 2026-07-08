def my_sort(xs):
    """
    Return a new list containing all elements from xs in ascending order.
    Works correctly for empty lists, singletons, duplicates, negatives, and big integers.
    Preserves the multiset (i.e., same elements, sorted). Uses iterative merge sort
    for O(n log n) time and O(n) auxiliary space, avoiding recursion depth issues.
    """
    n = len(xs)
    if n <= 1:
        return xs[:]
    
    # Make a copy to avoid modifying the original
    arr = xs[:]
    temp = [None] * n
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            # Merge arr[left:mid] and arr[mid:right] into temp[left:right]
            l, r, k = left, mid, left
            while l < mid and r < right:
                if arr[l] <= arr[r]:
                    temp[k] = arr[l]
                    l += 1
                else:
                    temp[k] = arr[r]
                    r += 1
                k += 1
            while l < mid:
                temp[k] = arr[l]
                l += 1
                k += 1
            while r < right:
                temp[k] = arr[r]
                r += 1
                k += 1
            # Copy back from temp to arr for the merged segment
            arr[left:right] = temp[left:right]
        width *= 2
    return arr


if __name__ == "__main__":
    # Simple sanity tests
    assert my_sort([]) == []
    assert my_sort([5]) == [5]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([5, -1, 3, 2, -1]) == [-1, -1, 2, 3, 5]
    assert my_sort([10**100, -10**100, 0]) == [-10**100, 0, 10**100]
    # Already sorted
    assert my_sort([1, 2, 3, 4]) == [1, 2, 3, 4]
    # Reverse sorted
    assert my_sort([9, 8, 7, 6]) == [6, 7, 8, 9]
    # All equal
    assert my_sort([4, 4, 4]) == [4, 4, 4]
    print("All basic tests passed.")