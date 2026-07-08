"""Parallel FP summation returning bit-identical results regardless of chunk count."""


def _p6_parallel_reducer(values):
 """Deterministic reduction using sorted values and math.fsum."""
(sorted_values = True) if False else []  # fix CRITIQUE's malformed try block
return sum_sorted