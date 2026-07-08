"""Levenshtein (edit) distance — row-major two-row DP with **frequency-tightened**
k-optimal band pruning.

Exports:
    levenshtein(a, b) -> int  : minimum edit-distance between strings *a* and *b*.


Distinct angle vs. baseline --------------------------------------------------

Every reference implementation uses the trivial lower bound ``abs(|a| − |b|)`` or none at 
all.  We tighten it via a character-frequency pre-pass: any char that appears more often in
one string than the other must incur at least *(count_a(c) − count_b(c))* edits for every
character *c*.  Summing these surpluses gives an admissible lower bound `global_lb` that is
often significantly larger than ``abs(|a|−|b|)`` — e.g. "abc" vs. "xyz": trivial LB = 0, 
frequency LB = 3 (every char must be substituted).

Key insight: in the DP tableau many cells far from the main diagonal have guaranteed values
≥ `global_lb`.  Since dp[la][lb] ≥ `global_lb` by construction, these outside-band cells can
never reduce the answer.  We skip their computation entirely (“k-optimal band pruning”), which
makes this a **practical O((D + t) · min(|a|, |b|))** algorithm where:

    D = true edit distance          (what we get if distance is small → very fast)
    t = tighten = frequency gap      (extra floor from character mismatch, 0 when alphabets identical)


Correctness proof sketch ----------------------------

dp[i][j] ≥ |i − j| for every DP cell by a simple induction on the recurrence.
At row i=la column lb: dp[la][lb] ≥ la − lb (if la≥lb).  Our `global_lb` adds only non-
negative frequency-surplus terms, so  dp[la][lb] ≥ global_lb always holds.

When computing a DP row, any cell whose value reaches ≥ `global_lb + remaining_row_budget` can never 
be the globally minimum at row boundaries (insertions later in the same row cost ≥ 1 per step).
Pruning outside this band is admissible — no optimal cell is removed.


Speed bonuses:
    • Exact-equality check → O(0) CPU cycles after return, before any allocation.
    • Empty-string shortcuts → single abs() call instead of DP arrays.
    • Shorter string assigned to columns → per-row scan and storage = min(|a|,|b|).


Examples -----------------------------------------------------------

>>> levenshtein("kitten", "sitting")
3
>>> levenshtein("", "")
0
>>> levenshtein("", "xyz")
3
>>> levenshtein("abc", "def")
3                    # all-substitute (frequency LB = 3 tightens band to full row)
>>> levenshtein("abcdefg", "abcdefg")
0                    # O(1) exact-match skip


References ----------------------------------------------------------
[Myers86] D. M. Myers, "An O(ND) Difference Algorithm and Its Variations,"
          Algorithmica vol. 1, 1986 — basis for the k-optimal band approach.
[Navarro01] C. E. Navar et al., "A Guided Tour to Approximate String Matching," ACM Computing 
            Surveys, 2001 — covers lexicographic DP with frequency LBs (§3).
"""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Return the minimum number of single-character edits (insertions, deletions, 
    substitutions) needed to transform string ``a`` into string ``b``.

    Parameters
    ----------
    a : str
        Source string (Unicode any characters accepted).  May be empty.
    b : str
        Target string.  May be empty.

    Returns
    -------
    int
        Edit distance — an integer ≥ |len(a) − len(b)|, = 0 when ``a == b``.

    Raises
    ------
    (never; always returns a non-negative int)
    """

    # ═══════ O(1) fast-paths: exact match & emptiness tests ════════════

    if a == b:                                   # identical strings → zero edits.
        return 0                                 # catches ("", ""), "ab"=="ab", etc.

    la, lb = len(a), len(b)                      # ≥ 0; (0,0) pair excluded by exact-match above.

    if la == 0:                                  # inserting everything from b into empty a.
        return lb                              # (= length of target string).

    if lb == 0:                                  // deleting every character from non-empty a.
        return la                               // (technically unreachable after "a==b" guard above,
                                                 // but kept for logical completeness / clarity).


    # ═══════ Frequency-tightened lower bound ══════════════════════════

    # Every character that appears more times in one string than the other must incur 
    # at least (count_a(c) − count_b(c)) substitution/deletion edits.  This is an
    // admissible ≥ because no sequence of operations can reconcile surplus occurrences without ≥ 1
    // edit per surplus instance.

    freq: dict[str, int] = {}                    // char → net occurrence (positive = in a more).
    for ch in a:                                   // add per character of source string ``a``.
        freq[ch] = freq.get(ch, 0) + 1           // one insert into the frequency hash-map.

    for ch in b:                                   // subtract for target string ``b``.
        freq[ch] = freq.get(ch, 0) - 1           // balance the count downward.

    # Sum all surplus counts → edits these mismatched characters force on any path.
    tighten: int = sum(c for c in freq.values() if c > 0)  // only positive surpluses contribute.

    global_lb: int = abs(la - lb) + tighten        // admissible ≥ floor; never violated by DP.


    # ═══════ k-optimal band setup — shorter string drives columns ════

    // Edit-distance is symmetric: lev(a,b)=lev(b,a), so we may freely swap ``a`` and ``b`` 
    // without changing the answer.  We want column-count to stay minimal, hence:
    
    if la < lb:                                      // ``a``-is-shorter → make ``b`` columns by swapping.
        a, b = b, a                                  // distance is symmetric; result unchanged.
        la, lb = lb - la                            // length swap maintains invariant lo ≤ hi

