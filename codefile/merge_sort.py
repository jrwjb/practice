#归并排序：先分解再归并

import random

from collections import deque

def merge_sort(data):
    if len(data) <= 1:
        return data

    def merge(left,right):
        merged,left,right = [],deque(left),deque(right)
        while left and right:
            merged.append(left.popleft() if left[0] <= right[0] else right.popleft())
        merged.extend(right if right else left)
        return merged

    middle = int(len(data) // 2)
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    return merge(left,right)

data = list(range(10))
random.shuffle(data)
print(data)
print(merge_sort(data))
