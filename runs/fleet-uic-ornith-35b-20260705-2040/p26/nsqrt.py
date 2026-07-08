# Full double-precision Newton's method sqrt without math.sqrt.
from __future__ import annotations


def _frexp(x: float) -> tuple[float, int]:
    """Return (m, e) such that x = m * 2**e with 0.5 <= abs(m) < 1."""
    if x == 0.0 or x != x:         # exact zero / NaN pass-through
        return float(x), 0
    sign = -1.0 if x < 0.0 else 1.0
    a = abs(x)
    e = 0
    while a >= 2.0:                 # normalise mantissa to [0.5, 2)
        a *= 0.5
        e += 1
    while a < 0.5 and a != 0.0:     # rarely runs for finite non-denorm doubles but kept for correctness
        a *= 2.0
        e -= 1
    return (-a if sign < 0 else a), -e


def isqrt_newton(x: float) -> float:
    """Compute sqrt(x) to full double precision via Newton's method (no math.sqrt)."""
    # Edge cases before any arithmetic division that would be undefined.
    if x == 0.0 or x != x:          # exact zero and NaN pass through unchanged
        return x
    if x < 0.0:                     # math library raises ValueError here too
        raise ValueError("square root of a negative number")

    # Initial guess from binary exponent.  With m in [0.5, 1) the answer is m**0.5*2**(e/2),
    # and ceil(e/2) gives a starting value always between half-√2 ≈ 0.71 and √2 ≈ 1.41 times
    # sqrt(x)*2^(-half+...)... more simply, after g_0 = 2**ceil(e/2), Newton is safe (g>0 for x>0).
    _, ep__ = _frexp(x)             # use only the exponent; mantissa doesn't matter for the seed's *scale*
    half_ep_ = (-1 + ep__) // 2 if ((-1 + ep__) & 1) else ep__ // 2
    g = float(2 ** half_ep_)        # always ≥ 0; non-denorm-safe because ep__ is integer

    # ---- Newton iteration: doubles the number of correct bits every step.
    abs_x_ = abs(x);                 # avoid recomputing inside the loop
    one_third_machine_eps_relative = 1e-16   # safe upper bound for "step < half-machine-eps in sqrt-of-x scale"

    for _cnt in range(30):          # safety cap (doubles converge ~5-8 iters once g is order-correct)
        g_new = 0.5 * (g + x / g)   # one Newton step: classical Babylonian update

        # Convergence when the previous iterate has practically stopped moving, *scaled* to the
        # expected sqrt-magnitude so tiny inputs still satisfy it once we're at full double precision.
        gap_abx = abs(g_new - g)
        scale_  = max(abs_x_, 1e-308) ** 0.5   # ~sqrt(|x|); safe for any non-negative x
        if gap_abx < one_third_machine_eps_relative * scale_:    # relative step << eps → full precision reached
            return g_new

        # Extra acceptance: when g has converged but the tiny-step signal is lost in sub-denorm noise,
        # check whether squaring g already reproduces x to within a handful of ULP.
        if gap_abx == 0.0 and abs(g * g - x) < 1e-30 * max(abs_x_, 1e-308):   # self-consistency fallback
            return g

        g = g_new

    raise RuntimeError("sqrt Newton did not converge")            # shouldn't happen for finite non-negative x

