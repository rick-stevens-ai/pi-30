from verify import Clock
from limiter import RateLimiter

clk = Clock()
rl = RateLimiter(rate=5, per=1.0, clock=clk)
print("Initial tokens:", rl.tokens, "capacity:", rl.capacity)
print("last_update:", rl.last_update)
# burst at t=0
allowed = sum(1 for _ in range(10) if rl.allow())
print("Allowed at t=0:", allowed, "tokens left:", rl.tokens)
print("last_update:", rl.last_update)
clk.advance(1.0)
print("After advancing 1.0, clk.t =", clk.t)
a2 = sum(1 for _ in range(10) if rl.allow())
print("Allowed after 1s:", a2, "tokens left:", rl.tokens)
print("last_update:", rl.last_update)
clk.advance(0.4)
print("After advancing 0.4, clk.t =", clk.t)
print("Before third phase: tokens =", rl.tokens, "last_update=", rl.last_update)
# Now let's manually iterate and print
print("\nDetailed for third phase:")
for i in range(10):
    before = rl.tokens
    allowed_now = rl.allow()
    after = rl.tokens
    print(f"Iter {i}: before={before:.15f}, allowed={allowed_now}, after={after:.15f}")
    # also print internal state
    print(f"    last_update={rl.last_update}, last_tokens? not stored")
