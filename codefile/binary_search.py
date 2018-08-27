#二分查找 :一种在有序数组中查找某一特定元素的搜索算法

import random

#while 循环
def binary_search(data,start,end,key):
    while start <= end:
        mid=start+(end-start)//2
        if data[mid] < key:
            start = mid + 1
        elif data[mid] > key:
            end = mid -1
        else:
            return mid



def binary(data,start,end,key):
    if start > end:
        return -1
    mid = start + (end - start) // 2
    if data[mid] > key:
        return binary(data,start,mid-1,key)
    if data[mid] < key:
        return binary_search(data,mid+1,end,key)
    return mid




data=list(range(100))
# random.shuffle(data)
print(len(data))

print(binary(data,0,len(data),20))