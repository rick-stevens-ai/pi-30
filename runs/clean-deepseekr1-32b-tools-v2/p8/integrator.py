import numpy as np

def rk4_solver(ode_func, t0, y0, step, h=1.0):
    k1 = ode_func(t0, y0)
    k2 = ode_func(t0 + 0.5*step*h, y0 + 0.5*k1*step*h)
    k3 = ode_func(t0 + 0.5*step*h, y0 + 0.5*k2*step*h)
    k4 = ode_func(t0 + step*h, y0 + k3*step*h)
    y_new = y0 + (1/6)*step*(k1 + 2*k2 + 2*k3 + k4)
    t_new = t0 + step*h  # Ensure exact time calculation
    return t_new, y_new

def solve(ode_func, t0, y0, total_time=100, h=1.0):
    solution = [(t0, y0)]
    step_num = 0
    while True:
        current_t, _ = solution[-1]
        if current_t >= t0 + total_time:
            break
        next_t = min(current_t + h, t0 + total_time)
        new_t, new_y = rk4_solver(ode_func, current_t, solution[-1][1], step_num+1, h)
        solution.append((next_t, new_y))
        step_num += 1
    return solution
