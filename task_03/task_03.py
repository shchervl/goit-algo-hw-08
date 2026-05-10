"""Task 03: minimal cost of merging cables, solved with a min-heap.

Optimal Merge Pattern.
Complexity: O(n log n) — each of n-1 merges does two pops and one push.
"""

import heapq
import random


def _validated_values(cables):
    """Return a list copy of `cables`, rejecting non-numeric or non-positive items."""
    result = []
    for c in cables:
        if not isinstance(c, (int, float)) or isinstance(c, bool):
            raise TypeError(f"cable length must be int or float, got {type(c).__name__}")
        if c <= 0:
            raise ValueError(f"cable length must be positive, got {c}")
        result.append(c)
    return result


def min_merge_cost(cables):
    """Return the minimal total cost of merging all cables into one.

    `cables` is an iterable of positive numbers (cable lengths).
    Returns 0 for an empty input or a single cable (no merges needed).
    Raises TypeError for non-numeric items, ValueError for non-positive ones.
    """
    heap = _validated_values(cables)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        cost = a + b
        total += cost
        heapq.heappush(heap, cost)
    return total


def naive_merge_cost(cables):
    """Total cost of merging cables left-to-right, without choosing order.

    Provided as a baseline to contrast with `min_merge_cost`. Each step
    appends the next cable to the running merged cable; the running
    length grows quickly and gets paid for again on every subsequent
    merge — usually significantly more expensive than the greedy plan.
    """
    cables = _validated_values(cables)
    if len(cables) < 2:
        return 0
    total = 0
    running = cables[0]
    for c in cables[1:]:
        running += c
        total += running
    return total


if __name__ == "__main__":
    cables = random.sample(range(1, 50), 10)
    greedy = min_merge_cost(cables)
    naive = naive_merge_cost(cables)

    print(f"{'Cable lengths:':<25}{cables}")
    print(f"{'Min cost (heap):':<25}{greedy}")
    print(f"{'Naive cost (left→right):':<25}{naive}")
    print(f"{'Savings:':<25}{naive - greedy} ({(naive - greedy) / naive:.1%})")
