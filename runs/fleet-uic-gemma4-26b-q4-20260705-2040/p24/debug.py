from limiter import RateLimiter

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

clk = Clock()
rl = RateLimiter(rate=5, per=1.0, clock=clk)
print(f"Initial: tokens={rl.tokens}, last_time={rl.last_time}")

allowed = sum(1 for _ in range(10) if rl.allow())
print(f"Step 1 (t=0): allowed={allowed}, tokens={rl.tokens}, last_time={rl.last_time}")

clk.advance(1.0)
a2 = sum(1 for _ in range(10) if rl.allow())
print(f"Step 2 (t=1.0): allowed={a2}, tokens={rl.tokens}, last_time={rl.last_time}")

clk.advance(0.4)
a3 = sum(1 for _ in range(10) if rl.allow())
print(f"Step 3 (t=1.4): allowed={a3}, tokens={rl.tokens}, last_time={rl.last_time}")
