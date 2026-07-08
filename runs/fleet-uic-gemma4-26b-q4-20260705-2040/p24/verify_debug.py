# P24 generator+critic: a token-bucket rate limiter that must NEVER allow more
# than `rate` events per `per` seconds in any window, using an injected clock.
# Seed resets naively each call (allows bursts beyond rate). Critic must catch
# the burst/refill bug.
from limiter import RateLimiter

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

def main():
    clk = Clock()
    rl = RateLimiter(rate=5, per=1.0, clock=clk)   # 5 per second
    allowed = sum(1 for _ in range(10) if rl.allow())  # all at t=0
    print(f"Loop 1: allowed={allowed}, tokens={rl.tokens}, last_time={rl.last_time}")
    if allowed != 5:
        print(f"BURST: allowed {allowed} at t=0, expected exactly 5")
        raise SystemExit(1)
    clk.advance(1.0)                                # full refill
    a2 = sum(1 for _ in range(10) if rl.allow())
    print(f"Loop 2: allowed={a2}, tokens={rl.tokens}, last_time={rl.last_time}")
    if a2 != 5:
        print(f"REFILL: allowed {a2} after 1s, expected 5")
        raise SystemExit(1)
    # partial refill: after 0.4s at rate 5/s, ~2 tokens back
    clk.advance(0.4)
    a3 = sum(1 for _ in range(10) if rl.allow())
    print(f"Loop 3: allowed={a3}, tokens={rl.tokens}, last_time={rl.last_time}")
    if a3 not in (2, 3):  # allow rounding either way
        print(f"PARTIAL: allowed {a3} after 0.4s, expected ~2")
        raise SystemExit(1)
    print("OK P24")

if __name__ == "__main__":
    main()
