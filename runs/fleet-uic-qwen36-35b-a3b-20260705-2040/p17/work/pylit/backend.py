"""pylit backend: any Python literal <-> repr / ast.literal_eval round-trip.

dumps(obj)  => repr(obj)         — any Python value serialised by its repr()
loads(s)    => ast.literal_eval) — stdlib-only parse, NEVER eval()
"""

import ast


def dumps(obj):
    """Serialize *obj* via repr().

    Parameters
    ----------
    obj : any Python value

    Returns
    -------
    str
        repr(obj), always a valid argument to ast.literal_eval.
    """
    return repr(obj)


def loads(s):
    """Parse string s as an ast literal, never using eval().

    Parameters
    ----------
    s : str

    Returns
    -------
    object
        The deserialised Python value (same rules as the CPython ast.literal_eval).
    """
    return ast.literal_eval(s)
