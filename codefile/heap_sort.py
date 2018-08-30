#堆排序

import random

def heap_sort(data):
    def sift(start,end):
        '''最大堆调整'''
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and data[child] < data[child + 1]:
                child += 1
            if data[root] < data[child]:
                data[root],data[child] = data[child],data[root]
                root = child
            else:
                break
    # 创建最大堆
    for start in range((len(data) - 2)):
        sift(start,len(data) -1)

    # 堆排序
    for end in range(len(data) -1,0,-1):
        data[0],data[end] = data[end],data[0]
        sift(0,end - 1)
    return data


data = list(range(10000))
random.shuffle(data)
print(data)
heap_sort(data)
print(data)