from limiter import TokenBucket

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

def test_token_bucket():
    clk = Clock()
    bucket = TokenBucket(rate=5, capacity=10, clock=clk)   # allow burst of 10 at t=0, refill at 5/s
    
    print(f"Initial: rate={bucket.rate}, capacity={bucket.capacity}, tokens={bucket.tokens}")
    
    allowed_count = 0
    for i in range(20):
        allowed = bucket.allow(n=1)
        if allowed:
            allowed_count += 1
        if allowed_count <= 15: # Print first few to debug
            print(f"Request {i+1}: {'ALLOWED' if allowed else 'DENIED'}, remaining={bucket.tokens}")
    
    print(f"Total allowed at t=0: {allowed_count} (expected max capacity=10)")
    
    clk.advance(1.0)  # full refill
    allowed_count_2 = 0
    for i in range(20):
        if bucket.allow(n=1):
            allowed_count_2 += 1
    print(f"After 1s advance: {allowed_count_2} additional allowed (expected max rate*1=5)")
    
test_token_bucket()