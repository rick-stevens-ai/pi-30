# P15 benchmark — prints Mtokens/s for top_k on 200k tokens.
import sys, time, random, string
from wordcount import top_k

def make():
    rng = random.Random(5)
    vocab = ["".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(2,6))) for _ in range(500)]
    return [rng.choice(vocab) for _ in range(200000)]

def main():
    report = "--report" in sys.argv
    toks = make()
    top_k(toks[:1000], 10)  # warm
    best = float("inf")
    for _ in range(3):
        t0 = time.perf_counter(); top_k(toks, 10); dt = time.perf_counter() - t0
        best = min(best, dt)
    mtps = len(toks) / best / 1e6
    print(f"{mtps:.4f}" if report else f"top_k 200k: {best*1e3:.1f} ms  {mtps:.3f} Mtok/s")

if __name__ == "__main__":
    main()
