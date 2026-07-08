from limiter import RateLimiter

class BackwardsClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def set(self, val):
        self.t = val

clk = BackwardsClock()
rl = RateLimiter(rate=1.0, per=2.0, clock=clk)  # capacity = 2
print("Initial:", rl.tokens, rl.last_update)
clk.set(0.0)
# first call at t=0
print("Allow 1 at t=0?", rl.allow(1))
print("Tokens after:", rl.tokens, "last_update:", rl.last_update)
# move clock backwards to t=-1 (unlikely but test)
clk.set(-1.0)
print("Clock set to -1")
print("Allow 1 at t=-1?", rl.allow(1))
print("Tokens after:", rl.tokens, "last_update:", rl.last_update)
# move clock forward to t=0.5
clk.set(0.5)
print("Clock set to 0.5")
print("Allow 1 at t=0.5?", rl.allow(1))
print("Tokens after:", rl.tokens, "last_update:", rl.last_update)
# move clock forward to t=1.5
clk.set(1.5)
print("Clock set to 1.5")
print("Allow 1 at t=1.5?", rl.allow(1))
print("Tokens after:", rl.tokens, "last_update:", rl.last_update)
