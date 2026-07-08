from limiter import RateLimiter

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

def main():
    clk = Clock()
    rl = RateLimiter(rate=5, per=1.0, clock=clk)
    
    print("--- BURST ---")
    allowed = []
    for i in range(10):
        res = rl.allow()
        allowed.append(res)
        print(f"t={clk()}, allow(): {res}, tokens: {rl.tokens}")
    print(f"Total allowed: {sum(allowed)}")

    print("\n--- REFILL ---")
    clk.advance(1.0)
    allowed = []
    for i in range(10):
        res = rl.allow()
        allowed.append(res)
        print(f"t={clk()}, allow(): {res}, tokens: {rl.tokens}")
    print(f"Total allowed: {sum(allowed)}")

    print("\n--- PARTIAL ---")
    clk.advance(0.4)
    allowed = []
    for i in range(10):
        res = rl.allow()
        allowed.append(res)
        print(f"t={clk()}, allow(): {res}, tokens: {rl.tokens}")
    print(f"Total allowed: {sum(allowed)}")

if __name__ == "__main__":
    main()
