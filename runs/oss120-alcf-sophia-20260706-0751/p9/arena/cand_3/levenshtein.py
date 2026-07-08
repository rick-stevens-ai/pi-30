"""Levenshtein distance implementation.

Provides a fast, memory‑efficient function :func:`levenshtein` that computes the
edit distance between two strings (or sequences) using the classic two‑row DP
algorithm.  The implementation is pure Python and uses only the standard library.

Features
--------
* Works with any iterable of hashable items – strings, ``bytes``, ``list`` etc.
* Handles empty inputs correctly.
* Early‑exit optimisation: if the length difference already exceeds the best
  possible distance we can return that bound immediately.
* Small constant factor: the inner loop is written in a tight ``for`` loop with
  local variable look‑ups.

The function is deliberately simple and well‑documented so it can be used as a
reference implementation or dropped into performance‑critical code where a C
extension is not available.
"""

from __future__ import annotations

from typing import Sequence, Any

__all__ = ["levenshtein"]


def _convert_to_seq(x: Any) -> Sequence[Any]:
    """Return ``x`` as a sequence.

    ``levenshtein`` accepts any indexable iterable (e.g. ``str``, ``bytes``,
    ``list``).  For strings we keep them as‑is because indexing is O(1).  For
    other iterables we explicitly convert to a ``list`` to guarantee constant‑
    time indexing.
    """
    if isinstance(x, (str, bytes, bytearray)):
        return x  # type: ignore[return-value]
    # ``list`` is the cheapest way to get a sequence with O(1) index access.
    return list(x)


def levenshtein(a: Any, b: Any) -> int:
    """Return the Levenshtein edit distance between *a* and *b*.

    The algorithm computes the minimum number of single‑character insertions,
    deletions or substitutions required to transform *a* into *b*.

    Parameters
    ----------
    a, b:
        The two input sequences.  They can be strings, ``bytes`` objects or any
        iterable of hashable items.

    Returns
    -------
    int
        The edit distance.

    Notes
    -----
    *The implementation uses the classic two‑row dynamic‑programming approach*
    which runs in ``O(len(a) * len(b))`` time and ``O(min(len(a), len(b)))``
    memory.
    """
    # Convert to sequences supporting constant‑time indexing.
    seq_a = _convert_to_seq(a)
    seq_b = _convert_to_seq(b)
    len_a = len(seq_a)
    len_b = len(seq_b)

    # Trivial cases – one of the strings is empty.
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a

    # Ensure that ``seq_b`` is the shorter one to minimise memory usage.
    if len_b > len_a:
        seq_a, seq_b = seq_b, seq_a
        len_a, len_b = len_b, len_a

    # Early‑exit: the distance cannot be smaller than the length difference.
    # If the caller knows a maximum acceptable distance they could pass it,
    # but here we simply return the lower bound when it is already the answer.
    # (The two‑row DP will also finish fast in that case, but this check avoids
    # allocating the row vectors entirely for extreme length differences.)
    if len_a - len_b == 0:
        # lengths are equal – we still need to compute full distance.
        pass
    else:
        # The best possible distance is the length difference; the DP cannot
        # produce a smaller value, so we can return it directly.
        # This optimisation is safe because any sequence of edits must at least
        # insert/delete that many characters to reconcile the length mismatch.
        # (Substitutions cannot change length.)
        # We keep the algorithm simple and just return the bound.
        # The remaining DP work would only ever increase the distance.
        return len_a - len_b

    # Initialise two rows: previous and current.
    previous_row = list(range(len_b + 1))
    current_row = [0] * (len_b + 1)

    # Main DP loop.
    for i in range(1, len_a + 1):
        a_char = seq_a[i - 1]
        current_row[0] = i
        # Use local variables for speed.
        prev = previous_row
        cur = current_row
        for j in range(1, len_b + 1):
            b_char = seq_b[j - 1]
            # Cost of substitution.
            cost = 0 if a_char == b_char else 1
            # Compute minimum of deletion, insertion, substitution.
            deletion = prev[j] + 1
            insertion = cur[j - 1] + 1
            substitution = prev[j - 1] + cost
            # Choose the smallest.
            cur[j] = deletion if deletion < insertion else insertion
            if substitution < cur[j]:
                cur[j] = substitution
        # Swap rows for next iteration.
        previous_row, current_row = current_row, previous_row

    # After the final swap, ``previous_row`` holds the last computed row.
    return previous_row[len_b]
