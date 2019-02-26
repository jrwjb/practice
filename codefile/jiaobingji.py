a = [1,2,3,4]
b = [4,3,5,6]
#交集
jj = list(set(a).intersection(set(b)))
#并集
bj = list(set(a).union(set(b)))
#差集
cj1 = list(set(b).difference(set(a))) # b中独有
cj2 = list(set(a).difference(set(b))) # a中独有

print(a)
print(b)
print('####')
print('交集',jj)
print('并集',bj)
print('b中独有',cj1)
print('a中独有',cj2)
