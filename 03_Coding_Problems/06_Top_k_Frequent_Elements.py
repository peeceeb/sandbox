from collections import Counter
import heapq
from multiprocessing import heap

def topKFrequent(nums, k):
    # Count how many times each number appears.
    frequency = Counter(nums)
    # Heap will store:
    # (-frequency, number)
    heap = []
    # Add every number and its frequency.
    for number, count in frequency.items():
        heapq.heappush(heap, (-count, number))

    result = []
    # Remove the k most frequent numbers.
    for _ in range(k):
        count, number = heapq.heappop(heap)
        result.append(number)
    return result