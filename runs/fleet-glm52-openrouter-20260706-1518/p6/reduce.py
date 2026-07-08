"""Bit-identical parallel reduction.

``parallel_sum(xs, nchunks)`` returns a result that is bit-identical no
matter how the data is partitioned into chunks.

Floating-point addition is *not* associative, so the naive approach — sum
each chunk separately, then combine the chunk totals — gives different
answers for different ``nchunks``.

Why this works
--------------
``math.fsum`` computes the *correctly rounded* sum of its entire input: it
keeps an exact (infinite-precision) running total and performs a single
final rounding to ``float``. The result is the closest float to the exact
mathematical sum of every element, and it does **not** depend on the order
or grouping of those elements.

The tempting "parallel" alternative — running ``math.fsum`` per chunk to
get partials and then combining those partials with another ``math.fsum``
— is *not* bit-identical across ``nchunks``: each per-chunk ``fsum`` is
already a rounded float, so different partitions yield different partials
and hence a different final value. Only feeding *every raw element* into a
single ``math.fsum`` avoids partition-dependent rounding.

So ``nchunks`` here controls only how the data is *traversed* (mimicking a
parallel chunked scan for I/O / memory locality), never how the math is
combined. Every element is forwarded — in fixed (data) order, with no
per-chunk rounding — into exactly one ``math.fsum`` call, so the returned
value is independent of ``nchunks`` and bit-identical across all partitions.

Memory stays bounded: elements are pulled from the iterable chunk by chunk
(a generator feeds ``math.fsum``), so the whole input is never materialized
at once, regardless of ``nchunks`` or input size. Works with any iterable,
including single-use generators, and *always* drains the entire iterable
even when its length is unknown.
"""

import math
from itertools import islice


def parallel_sum(xs, nchunks=1):
    """Return a bit-identical sum of ``xs`` regardless of ``nchunks``.

    The iterable is consumed in fixed (data) order, chunk by chunk, where
    the chunk boundaries are purely structural (they mirror how a parallel
    reduction would assign slices to workers) and never enter the
    arithmetic. Every raw element is handed to a single ``math.fsum``, so
    no partition-dependent rounding is ever introduced and the result is
    the closest float to the exact total — independent of ``nchunks``.
    """
    nchunks = 1 if not nchunks or nchunks < 1 else int(nchunks)
    it = iter(xs)

    # Prefer evenly sized slices derived from the known length so that
    # ``nchunks`` genuinely partitions the traversal. For unsized iterables
    # fall back to equal-count chunks; the count is irrelevant to the
    # result (only order matters), so a reasonable fixed size suffices.
    try:
        total = len(xs)
    except TypeError:
        total = None

    if total is not None:
        base, extra = divmod(total, nchunks)
        sizes = [base + (1 if i < extra else 0) for i in range(nchunks)]
        # Guard against a trailing zero-size chunk (nchunks > total) and
        # drain any remainder so the whole iterable is consumed exactly once.
        sizes.append(None)
    else:
        # Unknown length: keep pulling fixed-size slices until the iterable
        # is exhausted. nchunks only sets the *initial* traversal granularity
        # here; it never limits how much data is consumed, so a long
        # single-use generator is still summed in its entirety and the
        # result stays independent of nchunks.
        chunk = max(1, 1 << 20)
        sizes = [chunk] * nchunks
        sizes.append(None)

    def _chain():
        for size in sizes:
            if size is None:
                # Drain remainder (covers rounding / nchunks > total).
                for x in it:
                    yield x
                return
            if size <= 0:
                continue
            for x in islice(it, size):
                yield x

    # Single correctly-rounded reduction over *all* elements -> independent
    # of any partitioning, hence bit-identical across nchunks.
    return math.fsum(_chain())


if __name__ == "__main__":
    import random

    random.seed(42)
    xs = [
        random.choice([1e16, 1.0, -1e16, 3.14159, -2.71828, 1e-8])
        for _ in range(100000)
    ]
    seen = {parallel_sum(xs, n) for n in (1, 2, 3, 4, 7, 8, 16, 100)}
    print(len(seen), seen)
    # Sanity: works on a single-use generator too.
    assert parallel_sum(iter(xs), 13) == parallel_sum(xs, 1)
    # Sanity: edge cases are stable across nchunks.
    assert parallel_sum([], 5) == 0.0
    assert parallel_sum([1.0], 8) == 1.0
    assert {parallel_sum([1.0, 2.0, 3.0], n) for n in (1, 2, 3, 5, 100)} == {6.0}
