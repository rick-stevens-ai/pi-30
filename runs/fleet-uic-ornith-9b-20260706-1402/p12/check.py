# P12 oracle: base-N integer arithmetic. parse_int(s, base) and to_base(n, base)
# round-trip + match Python's int(s,base). Seed only handles base 10.
from baseconv import parse_int, to_base

def main():
    import random
    rng = random.Random(3)
    for _ in range(2000):
        n = rng.randint(0, 10**9)
        base = rng.randint(2, 36)
        s = to_base(n, base)
        # round trip
        if parse_int(s, base) != n:
            print(f"ROUNDTRIP FAIL n={n} base={base} got s={s} back={parse_int(s,base)}")
            raise SystemExit(1)
        # match python's reference for the digits we produced (lowercase)
        if int(s, base) != n:
            print(f"REF FAIL n={n} base={base} s={s}")
            raise SystemExit(1)
    # explicit edge cases
    assert to_base(0, 2) == "0", to_base(0, 2)
    assert to_base(255, 16) == "ff", to_base(255, 16)
    assert parse_int("ff", 16) == 255
    assert to_base(10, 2) == "1010"
    print("OK P12")

if __name__ == "__main__":
    main()
