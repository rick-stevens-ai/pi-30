"""
Count overlapping occurrences of ``needle`` in ``haystack``.

The function returns the number of times ``needle`` appears in ``haystack`` with
allowing overlaps, e.g. ``count_overlapping("aaaa", "aa")`` evaluates to 3.

If ``needle`` is an empty string the result is defined as ``0``
because matching an empty pattern does not make sense for a count.

The implementation uses :meth:`str.find` in a loop, advancing one character
after each match.  This gives linear‑time behaviour for typical input sizes
and is fast on very long strings because the underlying C search routines of
CPython are highly optimised.  No additional libraries are required.
"""

from __future__ import annotations

__all__ = ["count_overlapping"]


+def count_overlapping(haystack: str, needle: str) -> int:
+    """Return the number of overlapping occurrences of *needle* in *haystack*.
+
+    Parameters
+    ----------
+    haystack : str
+        The string to search.
+    needle : str
+        The substring to count.  An empty *needle* yields ``0``.
+
+    Returns
+    -------
+    int
+        The number of overlapping matches.
+    """
+
+    if not needle:
+        # Define count for an empty needle as 0 – matching an empty string at every position would be infinite.
+        return 0
+
+    count = 0
+    start_idx = 0
+    while True:
+        idx = haystack.find(needle, start_idx)
+        if idx == -1:
+            break
+        count += 1
+        # Advance by one to allow overlapping matches.
+        start_idx = idx + 1
+
+    return count
+
*** End of file ***"