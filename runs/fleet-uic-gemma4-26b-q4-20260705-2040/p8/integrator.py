def solve(f, y0, t0, t1, n):
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        # Compute t using t0 + step * h to avoid drift
        t = t0 + i * h
        
        k1 = h * f(t, y)
        k2 = h * f(t + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(t + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(t + h, y + k3)
        
        y += (k1 + 2*k2 + 2*k3 + k4) / 6.0
    
    return y
