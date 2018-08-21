#insert_sort :类似于抓牌，把后面无序的按大小插入到前面有序的列中

import random

def insert_sort(data):
    for i in range(1,len(data)):
        temp=data[i]
        j=i-1
        while j>=0 and data[j]>temp:
            data[j+1]=data[j]
            j=j-1
        data[j+1]=temp

data=list(range(10))
random.shuffle(data)
print(data)
insert_sort(data)
print(data)