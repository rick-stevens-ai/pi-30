from limiter import TokenBucket

class Clock:
    def __init__(self): 
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt

def test_token_bucket():
    clk = Clock()
    tb = TokenBucket(rate=5, capacity=3, clock=clk)  # Allow burst of 3 at most, refill at 5/s
    
    # Test initial burst - should allow exactly 3 (capacity)
    allowed_initial = sum(1 for _ in range(10) if tb.allow())
    print(f"Initial burst allowed: {allowed_initial}")
    assert allowed_initial == 3, f"Expected 3 at t=0, got {allowed_initial}"
    
    # Advance time by 1 second, should refill to capacity (5 tokens * 1s = 5, capped at capacity 3)
    clk.advance(1.0)
    allowed_after_1s = sum(1 for _ in range(10) if tb.allow())
    print(f"After 1s advance: {allowed_after_1s}")
    assert allowed_after_1s == 3, f"Expected 3 after 1s refill (capped at capacity), got {allowed_after_1s}"
    
    # Partial refill - advance by 0.2 seconds (should add ~1 token)
    clk.advance(0.2)
    allowed_after_partial = sum(1 for _ in range(10) if tb.allow())
    print(f"After partial (0.2s) refill: {allowed_after_partial}")
    assert allowed_after_partial <= 2, f"Expected at most 2 after 0.2s (1 token refill), got {allowed_after_partial}"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_token_bucket()