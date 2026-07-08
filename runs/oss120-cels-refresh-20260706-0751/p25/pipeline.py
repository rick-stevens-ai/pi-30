# Pipeline combining clean, agg, and fmt stages.

# Import the stage functions from their respective modules.
from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt


def run(rows):
    """Process *rows* through the three-stage pipeline.

    The pipeline performs:
        1. clean(rows) → list of floats, dropping non‑numeric values.
        2. agg(nums)   → dict with count, sum, mean, min, max.
        3. fmt(d)      → formatted "key=value" string with keys sorted.
    """
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted
