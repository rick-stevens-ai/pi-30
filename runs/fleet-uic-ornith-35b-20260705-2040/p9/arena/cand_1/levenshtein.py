"""Levenshtein edit distance — prefix/suffix stripping + two-row DP.

Distinct angle vs textbook implementations:

  * Most naive solutions build the full n×m matrix, but an optimal alignment
    always leaves shared leading/trailing characters untouched (the prefix/suffix
    never needs a substitution or insertion along any optimal cost path). So we
    strip them off and only run the real two-row DP on what's left — often much
    smaller.

  * Iterating with the shorter string as columns keeps the prev/curr vectors
    O(min(n, m)) for cache friendliness inside tight inner cores.

Two trivial early returns (empty / identical) + a post-strip "only insertions or
deletions remain" shortcut cover every edge case cleanly.
"""


def levenshtein(a: str, b: str) -> int:
    # ── empty-identical shortcuts                                     
    if a == b:
        return 0
    n, m = len(a), len(b)
    if not n or not m:                              # |remaining| deletes/inserts left exactly
        return max(n, m)

    # strip equal leading characters — every alignment pays zero for these positions  
    lp = 0
    while lp < n and lp < m and a[lp] == b[lp]:
        lp += 1

    # strip equal trailing characters from the end; stop before reaching the
    # already-prefixed block so we never double-count shared tail chars.      
    rhs = min(n, m) - lp                          # first free index in whichever core is shorter 
    ls = 0
    while n - 1 - ls >= rhs:                      # safety guard; loop always hits `break` on mismatch
        if a[n - 1 - ls] == b[m - 1 - ls]:
            ls += 1
        else:
            break

    la, lb = n - lp - ls, m - lp - ls             # inner core lengths              
    if la <= 0 or lb <= 0:                          # one side is entirely consumed → only ins/del count
        return abs(n - m)                          

    ac = a[lp:n - ls] if not ls else a[lp:]        
    bc = b[lp:m - ls] if ls else b[lp:]            
    la, lb = len(ac), len(bc)                       # keep explicit after slice guard above
    
    # orient so the shorter dim drives columns → smallest prev/curr vectors
    if la < lb:
        ac, bc = bc, ac
        la, lb = lb, la

    # ── two-row DP confined to the trimmed cores                     
    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)

    for i in range(1, la + 1):
        ai_c = ac[i - 1]                           # pre-fetched once per row iteration          
        curr[0] = i                                # cost of "strip out this row" to blank column        
        for j in range(1, lb + 1):                
            sub_cost = prev[j - 1] if ai_c == bc[j - 1] else prev[j - 1] + 1
            curr[j] = min(sub_cost, prev[j] + 1, curr[j - 1] + 1)
        prev, curr = curr, prev                    # row-swap; `curr` will be overwritten now              

    return prev[lb]                                  # last cell of the (swapped) prior-row → current result
