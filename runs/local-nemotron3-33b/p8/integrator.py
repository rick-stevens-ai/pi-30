import numpy as np

def solve(f, y0, t0, tf, h):
    """
    Integrate ODE dy/dt = f(t, y) using RK4 without accumulating time.
    
    Parameters
    ----------
    f : callable
        Function returning array-like derivative at (t, y).
    y0 : list or np.ndarray
        Initial condition at t = t0.
    t0 : float
        Start time.
    tf : float
        Desired final time.
    h : float
        Step size.

    Returns
    -------
    y_final : np.ndarray
        Approximation of y(tf).
    t_vals : np.ndarray
        Array of times from t0 to tf inclusive, stepping exactly h each iteration.
    """
    # Number of steps needed (must divide evenly for exact final time)
    n_steps = int(round((tf - t0) / h))
    if n_steps <= 0:
        raise ValueError("h must be positive and yield at least one step")
    
    y = np.asarray(y0, dtype=float)
    # Store times (including initial point)
    t_vals = [t0]
    
    for i in range(1, n_steps + 1):
        # Compute current time directly; never accumulate.
        t = t0 + i * h
        
        # Classic RK4 increments
        k1 = f(t, y)
        k2 = f(t, y + 0.5 * h * k1)
        k3 = f(t, y + 0.5 * h * k2)
        k4 = f(t, y + h * k3)
        
        # Advance solution
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t_vals.append(t)
    
    return y, np.array(t_vals)