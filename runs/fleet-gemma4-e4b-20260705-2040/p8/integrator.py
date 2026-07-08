import numpy as np

def rk4_step(f, t, y, h):
    """
    Performs one step of Runge-Kutta 4th order integration.

    Args:
        f (function): The ODE function f(t, y).
        t (float): Current time.
        y (np.ndarray): Current state vector.
        h (float): Step size.

    Returns:
        tuple: (new_y, new_t) where new_y is the updated state and new_t is the updated time.
    """
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)

    y_new = y + (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    # Compute new time t = t0 + step * h (never accumulate)
    t_new = t + h
    return y_new, t_new

def solve(f, t0, y0, t_end, h):
    """
    Solves the ODE system from t0 to t_end using RK4 integration.

    Args:
        f (function): The ODE function f(t, y).
        t0 (float): Initial time.
        y0 (np.ndarray): Initial state vector.
        t_end (float): Final time.
        h (float): Step size.

    Returns:
        tuple: (solution_history, final_state) where solution_history is a list of (t, y) tuples.
    """
    y = np.array(y0)
    solution_history = [(t, y)]

    while t < t_end:
        # Ensure the last step does not overshoot t_end significantly
        current_h = min(h, t_end - t)
        if current_h <= 1e-15: # Use a small tolerance check for floating point safety
            break

        y_new, t_next = rk4_step(f, t, y, current_h)
        t = t_next
        y = y_new
        solution_history.append((t, y))

    return y if isinstance(y, np.ndarray) and y.ndim == 0 else (y[0] if isinstance(y, np.ndarray) and y.size == 1 else y)

# Example usage (if needed for testing):
# def example_ode(t, y):
#     # Simple decay: dy/dt = -y
#     return np.array([-y[0]])

# t0 = 0.0
# y0 = np.array([1.0])
# t_end = 5.0
# h = 0.1

# history, final_y = solve(example_ode, t0, y0, t_end, h)
# print("Solution History:", history)
# print("Final State:", final_y)