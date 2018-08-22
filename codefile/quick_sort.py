#quick_sort :通过一趟排序将序列分成两部分，一部分都比temp小，一部分都比temp大

import random

def quick_sort(data,left,right):
    if left<right:
        mid=partition(data,left,right)
        quick_sort(data,left,mid-1)
        quick_sort(data,mid+1,right)

def partition(data,left,right):
    temp=data[left]
    while left<right:
        while left<right and data[right]>=temp:
            right-=1
        data[left]=data[right]
        while left<right and data[left]<=temp:
            left+=1
        data[right]=data[left]
    data[left]=temp
    return left

data=list(range(10))
random.shuffle(data)
print(data)
quick_sort(data,0,len(data)-1)
print(data)