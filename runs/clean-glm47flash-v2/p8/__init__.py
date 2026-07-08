"""Integrable package with RK4 ODE solver using explicit step-based time formula.

Test harness imports: from integrator import solve
"""

from .runner_solve as rk_integration

__all__: list[str] = ['mk_solver', 'rkolve']


# src/ runner-solver.py - core integration based on numerical-stability SKILL.md