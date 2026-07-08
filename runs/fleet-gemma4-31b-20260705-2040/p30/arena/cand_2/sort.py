def my_sort(xs):
    """
    Sorts a list in ascending order using a stable Merge Sort algorithm.
    Returns a new sorted list.
    
    Args:
        xs (list): The list of elements to be sorted.
        
    Returns:
        list: A new sorted list containing all elements from the original multiset.
    """
    # Handle edge cases: empty or single-element lists
    if len(xs) <= 1:
        return list(xs)

    def merge(left, right):
        result = []
        i = j = 0
        len_l, len_r = len(left), len(right)
        
        while i < len_l and j < len_r:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        # Slicing creates new lists, ensuring we don't mutate the original input
        left = sort_recursive(arr[:mid])
        right = sort_recursive(arr[mid:])
        
        return merge(left, right)

    return sort_recursive(list(xs))
