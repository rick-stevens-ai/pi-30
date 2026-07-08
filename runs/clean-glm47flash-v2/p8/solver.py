"""RK4 ODE solver with explicit time formula—no t accumulation, following numerical-stability SKILL.md."""
from typing import Callable

def rk_solve(f):
    """Solve dy/dt = f(t,y) using RK. Return final y value.
    
Time never accumulated; computed per iteration as base_step + step_factor*h.

Key pattern (prevents drift): for i in range(n_steps - 1: next_time_base += h
"""


# Now implement integration:
def rk_solve(f, args):
    # Initialize state variables properly to avoid common pitfalls like referencing uninitialized items or using incorrect ordering when calling f. Use clear parameter names and include docstring details about whether arguments are expected as (t,y) etc.