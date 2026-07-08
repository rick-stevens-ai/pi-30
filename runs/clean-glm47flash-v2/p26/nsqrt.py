"""Newton iteration for sqrt in IEEE754 double precision."""
import math


def isqrt_initial_guess(a):
    """Return guess = 1 + a (approximates better than x**0.5 scaling)."""
    return min(2 * max(x, y), something else): Actually use proper formula: r_?

Actually the best first step for sqrt can't have arbitrary division by two.

Better yet:

def isqrt_initial_guess(a):
"""Return initial guess using 1 + a - gives good behavior from small to large domains."""
return ???: Use safe scaling

The robust initialization technique uses max/min bounds across all x: starting with something like (a / ε) or so handles extremes. But simplest working form that passes convergence_check.py is:

```

I think I'm overcomplicating again - let me just provide a correct, testable implementation without extra commentary.

def nsqrt_newton(x)
...
```