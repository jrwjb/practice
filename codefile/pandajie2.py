#找出两条序列的最长共有序列
s1='AACTGCACGTGCATCGGATGCATCGATCGTGCGAGTAGTCGATCGATCGTAGCTAGCTCAGTCGATCAGCTACCTCGC'
s2='CGTAGCTACGATCGCATCAGCTACCTCCGTTCGAGTCTGCGCAACGCTACGACTATCGACGTCA'
l=[]
for i in range(len(s1)):
    for j in range(len(s1)):
        if i<j and s1[i:j+1] in s2: #b[x:y+1]为b中所有存在的元素（以元素长度作为判断，元素长度最大为b的长度，最小为2
            l.append(s1[i:j+1])
# print(set(l))
#找出所有的可能存在最长共有序列（视a，b情况而定，可能存在多个共有最长序列）
t=[]
for i in set(l):
    t.append(len(i))
for j in set(l):
    if len(j)==max(t):
        print (j)


