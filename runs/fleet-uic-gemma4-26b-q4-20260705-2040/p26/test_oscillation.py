def test_oscillation(x):
    if x == 0: return 0.0
    g = x if x > 1 else 1.0
    seen = set()
    for i in range(100):
        next_g = 0.5 * (g + x / g)
        print(f"Iter {i}: g={g}, next_g={next_g}")
        if next_g == g:
            print("Converged!")
            return g
        if next_g in seen:
            print("Oscillation detected!")
            return g
        seen.add(g)
        g = next_g
    print("Did not converge")
    return g

test_oscillation(2.0)
