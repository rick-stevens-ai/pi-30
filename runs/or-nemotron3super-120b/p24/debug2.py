class RateLimiterOrig:
    def __init__(self, rate, per, clock):
        self.rate = rate
        self.per = per
        self.clock = clock
        self.capacity = rate * per
        self.tokens = self.capacity
        self.last_update = self.clock()
    def allow(self, n=1):
        if n <= 0:
            return True
        now = self.clock()
        elapsed = now - self.last_update
        if elapsed < 0.0:
            elapsed = 0.0
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        if self.tokens >= n - 1e-9:
            self.tokens -= n
            if self.tokens < 0:
                self.tokens = 0.0
            return True
        return False

from verify import Clock
clk = Clock()
rl = RateLimiterOrig(5,1.0,clk)
print("initial:", rl.tokens, rl.last_update)
# burst at t=0
for i in range(5):
    print(f"before {i}: {rl.tokens}")
    rl.allow()
    print(f"after {i}: {rl.tokens}")
print("after burst:", rl.tokens, rl.last_update)
clk.advance(1.0)
print("after +1.0:", clk.t)
for i in range(5):
    print(f"before {i}: {rl.tokens}")
    rl.allow()
    print(f"after {i}: {rl.tokens}")
print("after second burst:", rl.tokens, rl.last_update)
clk.advance(0.4)
print("after +0.4:", clk.t)
print("before third:", rl.tokens, rl.last_update)
for i in range(5):
    print(f"iter {i}: before={rl.tokens}")
    allowed = rl.allow()
    print(f"  allowed={allowed}, after={rl.tokens}")
    print(f"  last_update={rl.last_update}")
