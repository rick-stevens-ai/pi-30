# P25 PLAN — fan-out: 3-stage stats pipeline.
# Each work/<stage>/stage.py exposes one function:
#   work/clean/stage.py : clean(rows) -> list[float]
#       drop any element that isn't convertible to float (None, "", "x" -> dropped)
#   work/agg/stage.py   : agg(nums) -> {"count":int,"sum":float,"mean":float,
#                                       "min":float,"max":float}
#   work/fmt/stage.py   : fmt(d) -> single line "k=v k=v ..." with keys ALPHA-sorted
# Integrator pipeline.py exposes:
#   run(rows) -> fmt(agg(clean(rows)))
# Acceptance: verify.py (DO NOT EDIT).
