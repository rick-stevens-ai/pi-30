# P17 PLAN — fan-out: 3 serializer backends + integrator codec.
# Each work/<fmt>/backend.py exposes:
#     dumps(obj) -> str
#     loads(s)   -> obj
# Backends:
#   csv   : obj is {"fields":[...]}; dumps -> "a,b,c"; loads -> {"fields":[...]}
#   kv    : obj is a flat {str:str}; dumps -> "k1=v1;k2=v2"; loads -> the dict
#   pylit : obj is any python literal; dumps -> repr(obj);
#           loads -> ast.literal_eval(s)   (stdlib ast only, never eval())
# Integrator codec.py exposes:
#     round_trip(fmt, obj) -> loads(dumps(obj)) using the matching backend.
# Acceptance: verify.py (DO NOT EDIT).
