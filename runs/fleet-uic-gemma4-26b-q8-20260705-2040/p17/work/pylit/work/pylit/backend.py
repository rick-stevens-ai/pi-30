import ast

def dumps(obj):
    return repr(obj)

def loads(s):
    return ast.literal_eval(s)
