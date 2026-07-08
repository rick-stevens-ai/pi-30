"""Count overlapping occurrences of needle in haystack.

Examples
--------
>>> count_overlapping("aaaa", "aa")
3  # Overlap counted

Empty input handling as specified.
"""


def _find_start_positions(haystack, start_idx):
    positions = []
```

Actually let me think this through simply. For counting overlaps:

The solution should be a simple generator-based approach:
1. If either string is empty (per spec), return 0
2. Iterate over all possible starting indices in haystack where needle could fit: `range(len(haystack) - len(needle))`
3. Count matches

Let me write it cleanly without extra helper functions which create complexity:

```python