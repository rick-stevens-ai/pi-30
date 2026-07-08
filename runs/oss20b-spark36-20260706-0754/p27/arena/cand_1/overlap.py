"""
A small utility for counting overlapping substring occurrences.

The standard :py:meth:`str.count` method counts **non‑overlapping** matches:
+>>> "aaaa".count("aa")
+1
+
+This module provides :func:`count_overlapping`, which counts all overlapping
+matches, including those that share characters.
+
+Examples
+--------
+>>> count_overlapping('aaaa', 'aa')
+3
+>>> count_overlapping('abababa', 'aba')
+2
+>>> count_overlapping('', 'a')
+0
+>>> count_overlapping('something', '')
+0
+
+The implementation is a one‑liner using the :mod:`re` module; the pattern
+``(?=needle)`` uses a positive look‑ahead, which allows matches that overlap.
+This keeps the code short, easy to understand and operates fully in C for
+speed – well suited for large strings.
+
+Only the Python standard library is used.  No external dependencies are
+lacked.
+"""
+
+from __future__ import annotations
+
+import re
+from typing import Iterable
+
+def count_overlapping(haystack: str, needle: str) -> int:
+    """Return the number of *overlapping* occurrences of ``needle`` in ``haystack``.
+
+    Parameters
+    ----------
+    haystack:
+        The string to search within.
+    needle:
+        The substring to find.  If an empty string is passed the function
+        returns ``0`` as per the contract in the problem statement.
+
+    Returns
+    -------
+    int
+        Count of overlapping matches.
+    """
+
+    if not needle:
+        # An empty needle by definition results in zero occurrences.
+        return 0
+
+    # ``re.escape`` ensures literal matching even if ``needle`` contains regex meta‑characters.
+    pattern = f"(?={re.escape(needle)})"
+    # Using ``finditer`` – each match is a zero‑width look‑ahead, so the match
+    # does not consume characters and subsequent matches can start at the next
+    # position.  The iterator yields all overlapping occurrences.
+    return sum(1 for _ in re.finditer(pattern, haystack))
+
+__all__: Iterable[str] = ["count_overlapping"]
+
*** End of file ***