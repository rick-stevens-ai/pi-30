# Orchestrate the three stages.

from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt

def run(rows):
    """Process *rows* through the stats pipeline.

    Equivalent to ``fmt(agg(clean(rows)))``.
    """
    return fmt(agg(clean(rows)))
