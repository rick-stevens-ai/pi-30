import ast


def dumps(obj) -> str:
    return repr(obj)


def loads(s) -> object:
    return ast.literal_eval(s)
