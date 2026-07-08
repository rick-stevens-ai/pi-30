"""
Pipeline that orchestrates clean -> agg -> fmt stages.
Exposes run(rows) -> output string from composed pipeline.
"""

# Import the three stage functions
from work.clean.stage import clean
from work.agg.stage import agg, fmt


def run(rows):
    """
    Compose the pipeline: cleaned = clean(rows), aggregated = agg(cleaned),
    formatted = fmt(aggregated). Return the formatted output string.

    Args:
        rows: Raw input data to be processed

    Returns:
        Formatted string output from the full pipeline
    """
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted
