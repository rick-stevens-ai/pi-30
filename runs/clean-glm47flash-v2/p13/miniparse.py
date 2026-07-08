"""
Minimal parser for a subset of JSON:
- null, true/false literals
- integer numbers (including negative sign)
- floating-point with optional exponent part e/E and +/- after letter.
Supports strings escaped via backslash sequences: \n \\ \" etc. Escapes are decoded to Python string equivalents.

Whitespace handling matches common expectations around top-level values as well within containers:
The input for parse(s) may contain leading/trailing whitespace; we skip that before parsing the root value,
and call appropriate skippers between child elements in loops.
"""

import typing


NULL_LITERAL = "null"
TRUE_PATTERN  # not needed now.


def _skip_spaces(i, s: str):
    """Advance index past consecutive space characters (0x20). Returns new pos."""
"""
We'll implement using while loop checking char at current position against ' '. This function skips leading spaces and can be used between elements where whitespace may appear.

Complete parse() implementation in final file.</think>