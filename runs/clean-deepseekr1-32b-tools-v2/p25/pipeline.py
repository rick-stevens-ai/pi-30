from work.clean.stage import CleanStage
from work.agg.stage import AggStage
from work.fmt.stage import FmtStage

def run(rows):
    clean_stage = CleanStage()
    agg_stage = AggStage()
    fmt_stage = FmtStage()
    
    cleaned_data = list(clean_stage(rows))
    aggregated_data = list(agg_stage(cleaned_data))
    formatted_output = fmt_stage(aggregated_data)
    
    return formatted_output
