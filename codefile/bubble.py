import random
import time

def timmer(func):
    def wrapper(*args,**kwargs):
        t1=time.time()
        func(*args,**kwargs)
        t2=time.time()
        return print(t2-t1)
    return wrapper

#冒泡排序：两两比较，大的（或小的）往上冒

#常规版
def bubble_sort(data):
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j]>data[j+1]:
                data[j+1],data[j]=data[j],data[j+1]

#优化版
@timmer
def bubble_sort2(data):
    for i in range(len(data)-1):
        flag=0
        for j in range(len(data)-i-1):
            if data[j]>data[j+1]:
                data[j+1],data[j]=data[j],data[j+1]
                flag=1

        if flag==0:
            break


data=list(range(10))
random.shuffle(data)
print(data)
bubble_sort2(data)
print(data)