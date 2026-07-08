from verify import Clock, RateLimiter

clk = Clock()
rl = RateLimiter(rate=5, per=1.0, clock=clk)
# burst at t=0
allowed = sum(1 for _ in range(10) if rl.allow())
print("Allowed at t=0:", allowed)
clk.advance(1.0)
a2 = sum(1 for _ in range(10) if rl.allow())
print("Allowed after 1s:", a2)
clk.advance(0.4)
# Now let's manually iterate and print
print("\nDetailed for third phase:")
for i in range(10):
    before = rl.tokens
    allowed_now = rl.allow()
    after = rl.tokens
    print(f"Iter {i}: before={before}, allowed={allowed_now}, after={after}")
