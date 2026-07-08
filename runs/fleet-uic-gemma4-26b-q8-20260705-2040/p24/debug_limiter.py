from limiter import RateLimiter

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

clk = Clock()
rl = RateLimiter(rate=5, per=1.0, clock=clk)
allowed_t0 = sum(1 for _ in range(10) if rl.allow())
print(f"t=0: {allowed_t0}")
clk.advance(1.0)
allowed_t1 = sum(1 for _ in range(10) if rl.allow())
print(f"t=1: {allowed_t1}")
clk.advance(0.4)
allowed_t14 = sum(1 for _ in range(10) if rl.allow())
print(f"t=1.4: {allowed_t14}")
