# P22 iterate-until-green: topological sort of a DAG with cycle detection.
# toposort(n, edges) -> a valid topological order (list) or raises ValueError on
# a cycle. Seed returns nodes in numeric order (ignores edges). Verdict=pytest.
from topo import toposort
import pytest

def is_valid_topo(n, edges, order):
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)

def test_linear():
    order = toposort(4, [(0,1),(1,2),(2,3)])
    assert is_valid_topo(4, [(0,1),(1,2),(2,3)], order)

def test_diamond():
    e = [(0,1),(0,2),(1,3),(2,3)]
    order = toposort(4, e)
    assert is_valid_topo(4, e, order)

def test_disconnected():
    e = [(1,0)]
    order = toposort(3, e)
    assert is_valid_topo(3, e, order)

def test_cycle_raises():
    with pytest.raises(ValueError):
        toposort(3, [(0,1),(1,2),(2,0)])

def test_self_loop_raises():
    with pytest.raises(ValueError):
        toposort(2, [(0,0)])
