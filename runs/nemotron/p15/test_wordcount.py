from wordcount import top_k
from collections import Counter
import random, string

def ref(tokens, k):
    return [w for w, _ in Counter(tokens).most_common(k)]

def make():
    rng = random.Random(5)
    vocab = ["".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(2,6))) for _ in range(500)]
    return [rng.choice(vocab) for _ in range(200000)]

def main():
    toks = make()
    got = top_k(toks, 10)
    exp = ref(toks, 10)
    gc = Counter(toks)
    if [gc[w] for w in got] != [gc[w] for w in exp]:
        print(f"WRONG top_k counts: got={[(w,gc[w]) for w in got]} exp={[(w,gc[w]) for w in exp]}")
        raise SystemExit(1)
    print("OK correct")

if __name__ == "__main__":
    main()
