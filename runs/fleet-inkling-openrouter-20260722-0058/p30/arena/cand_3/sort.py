"""Candidate #3 — iterative bottom-up merge sort (non-recursive, stdlib only)."""

def my_sort(xs):
    if not isinstance(xs, list):
        xs = list(xs)
    a = xs[:]  # preserve multiset, new list
    n = len(a)
    if n < 2:
        return a
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = a[i:i + width]
            right = a[i + width:i + 2 * width]
            merged = []
            l = r = 0
            while l < len(left) and r < len(right):
                if left[l] <= right[r]:
                    merged.append(left[l]); l += 1
                else:
                    merged.append(right[r]); r += 1
            merged.extend(left[l:])
            merged.extend(right[r:])
            a[i:i + len(merged)] = merged
        width *= 2
    return a
