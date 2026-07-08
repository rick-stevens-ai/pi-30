# P7 PLAN — the planner target. Workers each implement ONE parser backend to a
# shared interface, the integrator wires them into a dispatcher.
#
# Shared interface (each backend module exposes):
#     parse(text: str) -> dict
#
# Three backends, each in work/<name>/backend.py:
#   - csvbe   : parse a single CSV line "a,b,c" -> {"fields": ["a","b","c"]}
#   - kvbe    : parse "k1=v1;k2=v2" -> {"k1": "v1", "k2": "v2"}
#   - jsonbe  : parse a JSON object string -> the dict (stdlib json)
#
# Integrator (dispatch.py) exposes:
#     dispatch(kind: str, text: str) -> dict
#   kind in {"csv","kv","json"} routing to the matching backend.
#
# Acceptance is verify.py at the top level (DO NOT EDIT).
