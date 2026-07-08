"""RK4 ODE solve function implementing stable time update— follows numerical-stability SKILL.md."""


def rk_solve(f, y0, t_start):
    """One RK iteration: compute next state."""
    
# Test harness uses the main `solve` with explicit per-step timer computation.


import math
from typing import Callable

SOLVER = "rk4"


class Solver:

    

RETRY_STEP_METHOD_SIGNATURE_ERRORS:
"""Root cause analysis and lesson from encountering signature mismatch errors when creating solver modules. In solve(f, y0,tstart,h), arguments must strictly follow caller's expectations in calling code; otherwise ModuleNotFoundError or runtime type mismatches occur causing test failure."""


def main() -> None:

    f = lambda t,y: -2*t*y
"""
The primary issue preventing success was that multiple candidate implementation files had placeholder content with incorrect function signatures. When converge_check.py attempts to import solve(f, y0,t_end), but integrable/final_impl exposes a different call signature (e.g., no step count) or undefined behavior for t-update via per-step timer arithmetic rather than accumulation: callers receive runtime errors and tests break.

Solution pattern discovered through debugging `integrate` module. DO NOT edit converge_check.py—maintain target function interface solve(f, y0,tstep). Module-level variables should be defined to avoid NameError during import."""

    from integrable.sol for final value