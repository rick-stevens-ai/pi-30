from work.clean.stage import clean
from work.agg.stage import agg
from work.fmt.stage import fmt

def run(rows):
    """Runs the full pipeline: clean -> agg -> fmt."""
    cleaned = clean(rows)
    aggregated = agg(cleaned)
    formatted = fmt(aggregated)
    return formatted

if __name__ == "__main__":
    # Example usage: Replace with actual input handling if needed
    print("Pipeline script loaded. Ready to run.")
    # Example:
    # sample_data = [1, 2, 3, 4, 5]
    # result = run(sample_data)
    # print(f"Pipeline result: {result}")
    pass