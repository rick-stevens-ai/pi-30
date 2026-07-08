from verify import Clock, RateLimiter

clk = Clock()
rl = RateLimiter(rate=5, per=1.0, clock=clk)
print("Initial tokens:", rl.tokens, "capacity:", rl.capacity)
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
a3 = sum(1 for _ in range(10) if rl.allow())
print("Allowed after 0.4s more:", a3, "tokens left:", rl.tokens)
