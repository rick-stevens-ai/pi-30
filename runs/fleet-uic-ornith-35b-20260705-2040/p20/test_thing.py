# P20 iterate-until-green: LRU cache WITH per-entry TTL expiry.
# get(k) returns None if expired; put(k,v,ttl). Uses an injectable clock so tests
# are deterministic. Seed has no TTL at all. Verdict = pytest exit code.
from ttlcache import TTLCache
import pytest

class Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, dt): self.t += dt

def test_basic_get_put():
    clk = Clock(); c = TTLCache(capacity=2, clock=clk)
    c.put("a", 1, ttl=10)
    assert c.get("a") == 1

def test_expiry():
    clk = Clock(); c = TTLCache(capacity=2, clock=clk)
    c.put("a", 1, ttl=5)
    clk.advance(4); assert c.get("a") == 1
    clk.advance(2); assert c.get("a") is None     # expired at t=6 > 5

def test_lru_eviction():
    clk = Clock(); c = TTLCache(capacity=2, clock=clk)
    c.put("a", 1, ttl=100); c.put("b", 2, ttl=100)
    assert c.get("a") == 1            # a now MRU
    c.put("c", 3, ttl=100)           # evicts LRU = b
    assert c.get("b") is None
    assert c.get("a") == 1 and c.get("c") == 3

def test_expired_doesnt_count_against_capacity_on_access():
    clk = Clock(); c = TTLCache(capacity=1, clock=clk)
    c.put("a", 1, ttl=1)
    clk.advance(2)
    assert c.get("a") is None
    c.put("b", 2, ttl=10)
    assert c.get("b") == 2
