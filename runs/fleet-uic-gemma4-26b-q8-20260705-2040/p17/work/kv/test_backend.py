from backend import dumps, loads

def test():
    # Basic case
    d1 = {"k1": "v1", "k2": "v2"}
    s1 = dumps(d1)
    print(f"dumps({d1}) -> {s1!r}")
    assert s1 == "k1=v1;k2=v2"
    assert loads(s1) == d1

    # Empty dict
    d2 = {}
    s2 = dumps(d2)
    print(f"dumps({d2}) -> {s2!r}")
    assert s2 == ""
    assert loads(s2) == d2

    # Single item
    d3 = {"k": "v"}
    s3 = dumps(d3)
    print(f"dumps({d3}) -> {s3!r}")
    assert s3 == "k=v"
    assert loads(s3) == d3

    # Test trailing semicolon (if it happens)
    s4 = "k1=v1;k2=v2;"
    print(f"loads({s4!r})")
    try:
        res4 = loads(s4)
        print(f"Result: {res4!r}")
    except Exception as e:
        print(f"Failed with error: {e}")

if __name__ == "__main__":
    test()
