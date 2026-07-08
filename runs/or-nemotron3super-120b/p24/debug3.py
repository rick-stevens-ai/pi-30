from limiter import RateLimiter
from verify import Clock

clk = Clock()
rl = RateLimiter(5,1.0,clk)
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
