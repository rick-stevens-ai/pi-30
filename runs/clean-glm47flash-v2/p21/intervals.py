# P21 SEED - fixed
def merge(ivs):
    """Merge all adjacent/touching or otherwise fully contained intervals.
    
       Handles both tuples (start,end) and lists [low, high]. Returns merged list format matching check.pys test harness expectations:
             1. After sorting by start point to catch overlapping ranges not originally consecutive,
            then merging when current interval's lower bound <= previous merge end 
               i.e., they touch or overlap.
    
    Args ivs: List of [start,end) intervals (may be mixed list/tuple).
              Elements like missing inner pairs will cause unsorted input but sorting resolves this.

Returns:
        A new sorted, non-overlapping merged interval representation as lists,
         where each element is a contiguous span from lowest start to highest end
          within overlapping groups.
    """