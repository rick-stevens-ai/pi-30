# P21 oracle: merge overlapping intervals. Seed forgets to sort first and only
# merges adjacent-in-input intervals. Reference is a brute-force point-coverage
# check on small inputs.
from intervals import merge
import random

def ref_merge(ivs):
    if not ivs: return []
    s = sorted(ivs)
    out = [list(s[0])]
    for a, b in s[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [tuple(x) for x in out]

def main():
    rng = random.Random(21)
    for _ in range(2000):
        k = rng.randint(0, 8)
        ivs = []
        for _ in range(k):
            a = rng.randint(0, 20); b = a + rng.randint(0, 8)
            ivs.append((a, b))
        got = [tuple(x) for x in merge(list(ivs))]
        exp = ref_merge(ivs)
        if got != exp:
            print(f"MISMATCH in={ivs} got={got} exp={exp}")
            raise SystemExit(1)
    assert merge([]) == []
    assert [tuple(x) for x in merge([(1,3),(2,6),(8,10),(15,18)])] == [(1,6),(8,10),(15,18)]
    print("OK P21")

if __name__ == "__main__":
    main()
