from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt

def run(rows):
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted
