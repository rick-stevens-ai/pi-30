def topological_sort(graph):
    """
    Topologically sort using Kahn's algorithm.

    Args:
        graph: dict mapping node -> list of dependencies

    Returns:
            List containing nodes in valid order
"""
from collections import deque, defaultdict


class GraphError(ValueError):  # reuse/rename as desired.
"""Custom error class that will be raised on cycles etc.""" = None