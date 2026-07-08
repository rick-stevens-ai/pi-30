# P25 fan-out: a 3-stage stats pipeline, each stage a worker module.
#   work/clean/stage.py   : clean(rows) drops non-numeric, returns list[float]
#   work/agg/stage.py     : agg(nums) -> dict(count,sum,mean,min,max)
#   work/fmt/stage.py     : fmt(d) -> a sorted "key=value" string, keys alpha
# Integrator pipeline.py exposes run(rows) -> the formatted string.
from pipeline import run

def main():
    rows = ["1", "2", "x", "3", "", "4", None, "5"]
    out = run(rows)
    # expected: count=5 max=5.0 mean=3.0 min=1.0 sum=15.0  (alpha-sorted keys)
    parts = dict(p.split("=") for p in out.split())
    assert int(float(parts["count"])) == 5, out
    assert float(parts["sum"]) == 15.0, out
    assert float(parts["mean"]) == 3.0, out
    assert float(parts["min"]) == 1.0, out
    assert float(parts["max"]) == 5.0, out
    # keys must be alpha-sorted
    keys = [p.split("=")[0] for p in out.split()]
    assert keys == sorted(keys), f"keys not sorted: {keys}"
    print("OK P25")

if __name__ == "__main__":
    main()
