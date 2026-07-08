"""Pipeline module

Provides a single ``run`` function that wires together the three stages:
clean → agg → fmt.
"""

from __future__ import annotations

# Import the stage functions
from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt

__all__ = ["run"]


def run(rows: object) -> str:
    """Process *rows* through the pipeline and return a formatted string.

    The pipeline applies the ``clean`` stage to filter and convert the input
    rows to a list of ``float`` values, then aggregates those numbers with ``agg``
    and finally formats the resulting dictionary with ``fmt``.
    """
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted
