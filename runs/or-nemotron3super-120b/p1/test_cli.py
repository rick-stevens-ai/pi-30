import subprocess, sys, math

def run(stdin):
    p = subprocess.run([sys.executable, "cli.py"], input=stdin,
                       capture_output=True, text=True)
    return p.stdout.strip(), p.returncode

def parse(out):
    d = {}
    for tok in out.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = float(v)
    return d

def main():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    out, rc = run("\n".join(map(str, data)) + "\n")
    print(f"Output: {out}")
    assert rc == 0, f"nonzero exit {rc}: {out}"
    d = parse(out)
    assert int(d["count"]) == 8, d
    assert d["min"] == 2, d
    assert d["max"] == 9, d
    assert abs(d["mean"] - 5.0) < 1e-9, d
    assert abs(d["median"] - 4.5) < 1e-9, d
    assert abs(d["stdev"] - 2.138089935) < 1e-6, d
    print("OK P1")

if __name__ == "__main__":
    main()