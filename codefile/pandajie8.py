#找出基因列表中出现次数最多的基因
import time
start = time.clock()
with open(r'C:\Users\NB18040401\Desktop\gene.txt') as f:
    s=f.read().split()
    d={}
    for i in s:
        d.setdefault(i,0)
        d[i]+=1
    print(max(d.items(),key=lambda x:x[1]))
    stop=time.clock()
    print(stop-start)



# l=[1,2,3,4]
# def func(l):
#     l.insert(-1,'and')
#     for i in l:
#         print(i, end=',')
#     return
# func(l)

#计算字符串中每个字符出现的次数
# import pprint
# s='AAASSSDDDFFFGGHHHHTTTTTEE'
# count={}
# for i in s:
#     count.setdefault(i,0)
#     count[i]+=1
# # pprint.pprint(count)                          #使键排序输出
# print(count)                                    #输出每个字符出现的次数，返回对象为字典
# print(max(count,key=count.get))                 #输出出现次数最多的字符
# print(max(count,key=lambda x:count[x]))         #输出出现次数最多的字符
# print(max(count.items(),key=lambda x:x[1]))     #输出出现次数最多的字符及次数

#使用Counter()模块
# from collections import Counter
# c=Counter()
# for i in s:
#     c[i]+=1
# print(c)