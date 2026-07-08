EOF=6 # placeholder sentinel used above. Now writing final version.
cat > overlap_clean <<'PYSCRIPT'
#!/usr/bin/env python3
"""Count overlapping occurrences efficiently (KMP-based)."""

def _compute_lps(pattern: str) -> list[int]:
    """Longest prefix which is also a suffix for each position of pattern."""