"""
my_sort — bottom-up merge sort (two-buffer, Candidate #1 angle).

Key design decisions:
  · Two pre-allocated buffers alternate each pass → O(n) total allocation.
  · Slice-based drain at the end of merging replaces tight-element loops → massive CPython win.
  · Guaranteed O(n log n), stable, preserves multiset trivially (merge never drops/repeats).

Stdlib only.
"""


def my_sort(xs):
    """Return a *new* list with all values from *xs*, sorted ascending."""

    n = len(xs)
    if n <= 1:
        return list(xs)                       # fresh copy for empty / singleton edge cases

    buf_a = list(xs)                          # one copy of the input — src or dst each pass
    buf_b = [None] * n                        # partner buffer

    width = 1                                 # current run length
    while width < n:
        _merge_pass(buf_a, buf_b, width, len(buf_a))
        buf_a, buf_b = buf_b, buf_a           # swap roles for next pass
        width += width                      # double the gap (same as *= 2)

    return buf_a


def _merge_pass(src, dst, run_w, total):
    """Merge sort sweep: pairs of already-sorted sub-runs of length *run_w* are merged into *dst*.

    After this function returns the merged results live in dst[0 : total].
    """
    pos = 0                                  # walking pointer across data

    while pos < total:
        left_lo = pos
        left_hi = min(pos + run_w, total)     # exclusive end of left sub-run
        right_lo = left_hi                    # start of right sub-run (adjacent!)
        right_hi = min(right_lo + run_w, total)

        if left_lo == left_hi:              # only one sub-run at the tail — nothing to merge; just copy
            dst[pos:right_hi] = src[left_lo:right_hi]
        else:
            _merge(src, dst, left_lo, right_lo, right_hi)

        pos += run_w + run_w                # advance by two full-sized runs (may overshoot → loop exits cleanly)


def _merge(src, dst, lo, mid, hi):
    """Merge src[*lo*:mid] and src[mid:*hi*], write into dst[*lo*: *hi*].

    *stable*: equal elements in the left run are consumed before those of the right,
    preserving original relative order.
    Two-pass drain: copy remaining tail-ranges via slice-assignment for speed.
    """
    i, j = lo, mid           # read-heads: left  and right
    k = lo                   # write-head into dst

    while i < mid and j < hi:
        if src[j] < src[i]:       # strict < → stable (left wins on ties)
            dst[k] = src[j]
            j += 1
        else:
            dst[k] = src[i]
            i += 1
        k += 1

    # Remaining tail — at most one survives; copy via fast slice
    if i < mid:
        dst[k:mid + hi - j] = src[i:mid]
    elif j < hi:
        dst[k:] = src[j:hi]
