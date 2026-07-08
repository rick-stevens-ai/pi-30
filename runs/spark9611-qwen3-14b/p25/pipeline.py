import work.clean.stage as clean
import work.agg.stage as agg
import work.fmt.stage as fmt

def run(rows):
    cleaned = clean.process(rows)
    aggregated = agg.process(cleaned)
    formatted = fmt.process(aggregated)
    return formatted