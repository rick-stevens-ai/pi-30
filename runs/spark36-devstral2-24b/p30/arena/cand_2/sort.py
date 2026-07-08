"""
My sort using my_sort, stdlib only
"""
import random

def _median_of_three(a: list, lo: int, hi: int) -> tuple[int, int]:
    """
    Find median of three with their original indices.
    Returns (MedianValue, IndexOfMedian)
    """
    mid = (lo + hi) // 2
    if a[lo] > a[mid]:
        lo, mid = mid, lo
    if a[mid] > a[hi]:
        return _select_two_mixed((a[hi], hi), _select_two_mixed((a[lo], lo), (a[mid], mid)))
    else:
        return a[mid], mid

def _select_two_mixed(pair1: tuple[int, int], pair2: tuple[int, int]) -> tuple[int, int]:
    """
    Select one of two (value, index) pairs based on value.
    Returns the pair with smaller value, or pair2 if equal.
    """
    if pair1[0] < pair2[0]:
        return pair1
    else:
        return pair2

def _median_of_six(a: list, lo: int, hi: int) -> tuple[int, int]:
    """
    Median of six sample positions by 1/3 and 2/3 quantiles.
    Returns (MedianValue, IndexOfMedIndex)
    """
    span = hi - lo
    n4 = span // 4
    nh = span // 2
    a_offs = _index_a(lo, n4)
    b_offs = _index_b(lo, n4, nh)
    c_offs = _index_c(lo, hi, n4, nh)
    i0, m0 = _median_of_three(a, a_offs[1], a_offs[2])
    i1, m1 = _median_of_three(a, b_offs[1], b_offs[2])
    _, mi = _select_two_mixed((i0, m0), (i1, m1))
    return _median_of_three(a, a_offs[mi//2 + 1], c_offs[mi%2 + 1])

def _index_a(lo: int, n4: int) -> tuple[int, ...]:
    """
    Index sequence covering the first 3/4 region.
    """
    return (lo, lo+n4, lo+2*n4, lo+3*n4)

def _index_b(lo: int, n4: int, nh: int) -> tuple[int, ...]:
    """
    Index sequence covering the middle 1/2 region.
    """
    return (lo + n4, lo + n4 + nh//4, lo + n4 + 2*nh//4, lo + nh)

def _index_c(lo: int, hi: int, n4: int, nh: int) -> tuple[int, ...]:
    """
    Index sequence covering the last quarter.
    """
    return (lo + nh, hi - 3*n4, hi - 2*n4, hi - n4)

def my_sort(xs: list) -> list:
    """
    Sorting that is robust to emptiness, uniqueness, duplicates,
    negative integers and big integers while preserving multiset
    of elements. Performant on largeish arrays (N ~> 10^5).
    
    Strategy: Introsort using stdlib only.
    """
    if not xs:
        return []
    a = list(xs)      # defensive copy
    _sort_inplace(a, 0, len(a)-1)
    return a

def _sort_inplace(a: list[int], lo: int, hi: int):
    """
    Mutates a[lo..hi] with an introsort, using heap for depth control.
    """
    # Base cases handled at the top
    if lo >= hi:
        return

    max_depth = 2 * _msb(len(a)-1) + 3
    _intro_sort_loop(a, lo, hi, max_depth)

def _msb(n: int) -> int:
    """
    Counts most significant bit (1-relative) for powers of two.
    For any n > 0, returns k s.t. 2**(k-1) <= n < 2**k
    """
    if n == 0:
        return 0  # handle n==0 explicitly
    cnt = 0
    while n > 0:
        n >>= 1
        cnt += 1
    return cnt

def _intro_sort_loop(a: list[int], lo: int, hi: int, depth_limit: int):
    """
    Recursive loop of intro sort. Switches to heapsort when limit reached.
    """
    while True:
        if (hi - lo) <= 20:
            # small partition -> insertion to avoid overhead
            _insertion_sort_range(a, lo, hi)
            break
        depth_limit -= 1
        if depth_limit < 0:
            # too deep -> heapconvert
            _heapify_into_maxHeap(a, lo, hi)
            while hi > lo:
                a[lo], a[hi] = a[hi], a[lo]
                hi -= 1
                _sift_down(a, lo, hi-1)
            break
        # pick median of six for pivot, partition and recurse on smaller side first
        _, pix_idx = _median_of_six(a, lo, hi)
        a[pix_idx], a[lo] = a[lo], a[pix_idx]
        px_val = a[lo]
        l, r = lo + 1, hi
        while l <= r:
            if a[l] > px_val and a[r] < px_val:
                a[l], a[r] = a[r], a[l]
                l += 1
                r -= 1
            elif a[l] == px_val:
                l += 1
            elif a[r] == px_val:
                r -= 1
            else:
                if a[l] < px_val:
                    l += 1
                if a[r] > px_val:
                    r -= 1
        mid = r + 1
        a[lo], a[mid - 1] = a[mid - 1], a[lo]
        # recurse smaller chunk first to limit max stack depth
        left_len, right_len, mid_0 = (mid - lo-1), (hi-mid+1), mid
        if left_len <= right_len:
            _intro_sort_loop(a, lo, mid-2, depth_limit)
            lo = mid
        else:
            _intro_sort_loop(a, mid, hi, depth_limit)
            hi = mid - 2

def _heapify_into_maxHeap(a: list[int], lo: int, hi: int):
    """
    Convert a[lo..hi] into a max-heap in-place.
    After this, the parent/child invariant holds for all nodes >= (lo+hi)/2 .
    """
    n = hi - lo + 1
    start_idx = hi // 2 + (hi % 2 != 0)   # n//2 rounded up to floor of middle child
    for i in range(start_idx, lo-1, -1):
        _sift_down(a, lo, i)

def _sift_down(a: list[int], lo: int, idx: int):
    """
    Sifts element at a[idx] down to correct position preserving heap property.
    """
    val = a[idx]
    while idx < (lo + hi) // 2:
        left = 2*idx - lo
        right = left+1 if left < len(a)-1 and (left-lo + 2) <= (hi-lo+1)//2 else -1
        largest = idx
        if a[left] > a[largest]:
            largest = left
        if right != -1 and a[right] > a[largest]:
            largest = right
        if largest == idx:
            break
        a[idx], a[largest] = a[largest], a[idx]
        idx = largest

def _insertion_sort_range(a: list[int], lo: int, hi: int):
    """
    Standard insertion sort on the slice a[lo..hi].
    """
    for i in range(lo+1, hi+1):
        val = a[i]
        j = i-1
        while j >= lo and a[j] > val:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = val