import work.clean.stage as clean_stage
import work.agg.stage as agg_stage
import work.fmt.stage as fmt_stage

def run(rows):
    """
    Executes the pipeline: fmt(agg(clean(rows)))
    """
    cleaned_data = clean_stage.clean(rows)
    aggregated_data = agg_stage.agg(cleaned_data)
    formatted_data = fmt_stage.fmt(aggregated_data)
    return formatted_data

if __name__ == "__main__":
    # Example usage (assuming 'test_rows' is defined elsewhere or passed)
    print("Pipeline loaded successfully.")