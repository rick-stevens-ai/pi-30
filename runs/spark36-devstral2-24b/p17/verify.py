# P17 fan-out: three serializer backends to a shared interface, then a codec.
# work/<fmt>/backend.py exposes dumps(obj)->str and loads(str)->obj for fmt in
# {csv, kv, pylit}. Integrator codec.py exposes round_trip(fmt, obj) -> obj.
#   csv:   {"fields":[...]} <-> "a,b,c"
#   kv:    flat str->str dict <-> "k1=v1;k2=v2"
#   pylit: any literal <-> repr() / ast.literal_eval round trip
from codec import round_trip

def main():
    assert round_trip("csv", {"fields": ["a", "b", "c"]}) == {"fields": ["a", "b", "c"]}
    assert round_trip("kv", {"k1": "v1", "k2": "v2"}) == {"k1": "v1", "k2": "v2"}
    assert round_trip("pylit", {"x": [1, 2, {"y": (3, 4)}]}) == {"x": [1, 2, {"y": (3, 4)}]}
    assert round_trip("pylit", [1, "two", 3.0, None, True]) == [1, "two", 3.0, None, True]
    print("OK P17")

if __name__ == "__main__":
    main()
