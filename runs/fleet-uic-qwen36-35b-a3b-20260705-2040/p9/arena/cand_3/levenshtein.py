"""Candidature #3 — Bit-parallel Myers/Skiena for Levenshtein(costs<=1).

Distinct angle: compresses each DP row into a bit-vector (Python int arbitrary-width)
and updates the entire vector per character using bitwise ops — no inner Python loop.
O(n*m/w) word-parallel time via integer bit-vectors.

Algorithm: Myers "bit-vector edit distance" adapted for Levenshtein with unit costs.

Each DP-row entry h[k] = min cost in row i at col k is tracked implicitly by the
bitmasks Vx, Hy, Hn (see the algorithm below). The final answer is popcount(Hy<<slen)."""


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between a and b."""

    # --- trivial / identity shortcuts -----------------------------------
    if a == b:  # covers both-empty & identical strings
        return 0
    n, m = len(a), len(b)
    if n + m == 0:
        return 0
    if n == 0 or m == 0:
        return max(n, m)

    # --- choose shorter as columns to keep bit-vector narrowest ----------
    short, long_ = (a, b) if n <= m else (b, a)
    slen, len_ = min(n,m), max(n,m)  # fix: this was wrong in draft
