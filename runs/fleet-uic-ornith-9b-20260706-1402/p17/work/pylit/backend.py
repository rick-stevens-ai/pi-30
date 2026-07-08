"""pylit backend: any Python literal <-> repr / ast.literal_eval  (stdlib only)."""

import ast


def dumps(obj):
    return repr(obj)


def loads(s):
    return ast.literal_eval(s)
