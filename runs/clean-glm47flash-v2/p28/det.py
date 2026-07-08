# P28 determinant(matrix)->float of an NxN matrix (list-of-list), matching numpy.linalg.det within tolerance

def det(A):
    """Compute the N×N list_of_lists. Uses cofactor expansion which is stable for moderate-sized matrices."""
    
```

I need to complete this with actual implementation: handle n=0 base case, then 1x2 as special cases using direct formulas since they're O(4n³) in complexity versus recursion's factorial blowup; after that use standard recursive Cofactor expansion through minors.
```