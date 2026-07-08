from verify import Clock
from limiter import RateLimiter

clk = Clock()
rl = RateLimiter(rate=2.0, per=1.0, clock=clk)  # capacity=2
print("Capacity:", rl.capacity)
# try to take 3 at t=0 (should fail)
print("Allow 3 at t=0?", rl.allow(3))
# take 2 (should succeed)
print("Allow 2 at t=0?", rl.allow(2))
print("Tokens after:", rl.tokens)
# try to take 1 more (should fail because empty)
print("Allow 1 after empty?", rl.allow(1))
# wait 1 sec
clk.advance(1.0)
print("After 1 sec, tokens:", rl.tokens)
print("Allow 1 now?", rl.allow(1))
print("Tokens after:", rl.tokens)
# try to take 2 now (should fail because only 1)
print("Allow 2 now?", rl.allow(2))
# wait another sec
clk.advance(1.0)
print("After another sec, tokens:", rl.tokens)
print("Allow 2 now?", rl.allow(2))
