"""Integrate ODEs with stability-focused solver.

Test harness expects: from integor import solve
"""

from .runner_solve as rk_integrator

__all__: list[str] = ['solve']

# This file ensures proper module resolution in Python namespace.
def __getattr__(name):
    if name == 'solver':
        return None  # Placeholder for test compatibility - actual integration goes to runner_resolve.
