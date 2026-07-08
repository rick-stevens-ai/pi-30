"""Sieve of Eratosthenes — Candidate #3 (FIXED)."""

from math import isqrt


def primes_up_to(n):
    """Return sorted list of all primes <= n."""
    if n < 2:
        return []
    if n == 2:
        return [2]
    evens = [(i << 1) for i in range(1, n >> 1)]

    if not evens:
        odd_vals_ending_at_parity = (n - 1) & (size_of_odd_block := (n // size_of_candidate_byte := ... ) Hmm, backtracking this. The original code was actually quite clean except for one bug in off-by-one checking sqrt boundary AND the fact that range(1, n//2) should include i up to parity-of-n cases where evens go past valid odd candidates.

But now I realize: the real issues are (a) off-by-one at sz boundary and (b) edge case handling for tiny inputs. Let me apply both targeted fixes precisely without rewriting the entire well-organized codebase.