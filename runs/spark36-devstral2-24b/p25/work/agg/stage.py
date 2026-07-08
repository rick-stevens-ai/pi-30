import sys
from typing import List, Dict, Any, Optional


def clean(rows: List[Any]) -> List[float]: 
    """
    Clean the input rows by converting valid float elements to float,
    dropping any element that is not convertible (None, '', 'x') etc.
    Returns list of cleaned floats.
    """
    cleaned: List[float] = []
    # Traverse each row in rows
    for row in rows:
        # Support both dict-like and non-dict row structures based on the first element
        if isinstance(row, dict):
            num_candidate = row.get('num', None)
        else:
            num_candidate = row[0]  # Assume numeric value is at index 0 for simplicity
        
        # Convert to float while filtering non-convertible elements
        try:
            fval: Optional[float] = None
            if isinstance(num_candidate, str):
                if num_candidate.strip() == '':
                    continue  # Drop empty strings
                fval = float(num_candidate)
            else:
                fval = float(num_candidate)
        except (ValueError, TypeError):
            continue  # Drop non-convertible elements like None, 'x'
        
        cleaned.append(fval)
    
    return cleaned


def agg(nums: List[float]) -> Dict[str, Any]: 
    """
    Aggregate a list of numbers into {count, sum, mean, min, max}.
    Returns None for undefined values (e.g., when nums is empty).
    """
    if not nums:
        return {'count': 0, 'sum': float(0.0), 'mean': None, 'min': None, 'max': None}

    count = len(nums)
    total_sum = sum(nums)
    mean_val = total_sum / count
    minimum = min(nums) if nums else None
    maximum = max(nums) if nums else None

    return {'count': count, 'sum': total_sum, 'mean': mean_val, 'min': minimum, 'max': maximum}


def fmt(d: Dict[str, Any]) -> str: 
    """
    Format the dictionary as a single line of 'k=v' pairs,
    with keys sorted alphabetically.
    """
    items = []
    for k in sorted(d.keys()):
        v = d[k]
        if v is None:
            items.append(f'{k}=None')
        else:
            items.append(f'{k}={v}')
    
    return ' '.join(items)


if __name__ == '__main__':
    # Example usage
    rows = [1, 2, '3', None, '', ['x']]
    cleaned = clean(rows)
    print(f'cleaned: {cleaned}')

    aggregated = agg(cleaned)
    print(f'aggregated: {aggregated}')
    
    formatted = fmt(aggregated)
    print(f'formatted: {formatted}')
