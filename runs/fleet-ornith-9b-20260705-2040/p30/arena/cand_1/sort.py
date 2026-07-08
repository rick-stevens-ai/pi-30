"""Candidate #1 — Radix Sort (non-comparison based).

Stable, linear-ish O(n * k) for integer keys where k = number of digits.
Handles arbitrary Python ints natively; negatives via two-pass strategy.
Pure stdlib, iterative, cache-friendly on large arrays.
"""


def _radex(xs):
    """Non-comparison integer sort (Radix + LSD). Handles negatives."""
    if not xs:
        return []

    # Split into negative and non-negative so the digit-extraction trick works uniformly.
    pos = [x for x in xs if x >= 0]
    neg = [-x for x in xs if x < 0]  # sort ascending by absolute value → descending by actual value

    # ---- Radix sort on non-negative integers (LSD, base-256 buckets) ----
    def _radix_pass(a):
        """Sort list `a` of non-negative ints in place via LSD radix."""
        if len(a) <= 1:
            return a
        # Find max to bound the number of passes.
        m = max(a)
        if m == 0:
            return
        length = m.bit_length() // 8 + 1

        for shift in range(0, length * 8, 8):
            buckets = [[] for _ in range(256)]
            mask = (1 << 8) - 1
            for val in a:
                bkt = (val >> shift) & mask
                buckets[bkt].append(val)
            # Reassemble
            new_a = []
            for bkt in buckets:
                new_a.extend(bkt)
            a[:] = new_a

    _radix_pass(pos)

    # ---- Radix sort on absolute values of negatives, then negate back ----
    if neg:
        _radix_pass(neg)
        neg.reverse()  # descending order by magnitude
        for i in range(len(neg)):
            neg[i] = -neg[i]  # convert back to actual negative numbers

    # ---- Merge the two halves (negatives first, then positives) ----
    i = j = 0
    out = []
    while i < len(neg) and j < len(pos):
        if neg[i] < pos[j]:
            out.append(neg[i])
            i += 1
        else:
            out.append(pos[j])
            j += 1
    # Drain whichever list still has elements.
    while i < len(neg):
        out.append(neg[i]); i += 1
    while j < len(pos):
        out.append(pos[j]); j += 1

    return out


def my_sort(xs):
    """Return a new sorted (ascending) copy of *xs*.

    Preserves the multiset, correct on empty / singleton / duplicate /
    negative / big-int inputs. Runs in O(n · k) time for integer keys
    where k = number of base-256 digits — fast and cache-friendly on
    large arrays. Pure stdlib, no recursion.
    """
    return _radex(xs)
