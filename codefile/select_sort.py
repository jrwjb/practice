#选择排序：依次遍历整个序列取出最小（或最大）

import random

def select_sort(data):
    for i in range(len(data)-1):
        min_loc=i
        for j in range(i+1,len(data)):
            if data[j]<data[min_loc]:
                min_loc=j
        data[i],data[min_loc]=data[min_loc],data[i]


data=list(range(100))
random.shuffle(data)
print(data)
select_sort(data)
print(data)