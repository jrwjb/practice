#点突变计数
# with open(r'C:\Users\NB18040401\Desktop\rosalind_hamm.txt') as f:
#     s = f.__next__()
#     t = f.__next__()
#     c=0
#     for i in range(len(s)):
#         if s[i]!=t[i]:
#             c+=1
#     print(c)

#孟德尔第一定律
#有三个亲本（AA, Aa,aa）各两人，随机选择 两个亲本，1个后代个体表现显性性状的概率
# def f(x,y,z):
#     s=x+y+z
#     c = s * (s - 1) / 2.0
#     p=1-(z * (z - 1) / 2 + 0.25 * y * (y - 1) / 2 + y * z * 0.5) / c
#     return p
# print(f(18,22,27))

#RNA翻译蛋白
# rna='AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA'
# with open(r'C:\Users\NB18040401\Desktop\rosalind_prot.txt') as f:
#     rna=''.join(f.read().split('\n'))
#     codonTable = { 'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M', 'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T', 'AAC': 'N', 'AAU': 'N', 'AAA': 'K', 'AAG': 'K', 'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R', 'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L', 'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P', 'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R', 'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V', 'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A', 'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E', 'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G', 'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S', 'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L', 'UAC': 'Y', 'UAU': 'Y', 'UAA': '', 'UAG': '', 'UGC': 'C', 'UGU': 'C', 'UGA': '', 'UGG': 'W', }
#     l=[]
#     s=''
#     for i in range(0,len(rna),3):
#         l.append(rna[i:i+3])
#     for j in l:
#         s+=codonTable[j]
#     print(s)

#find a motif in dna
# seq = 'CGGGCATCTCGGGCATCTAAACGGGCATTTCGAATCACCGGGCATATAACGGGCATCGGGCATCGGGCATCGGGCATGGCGGGCATCGGGCATGATCGGGCATCGGGCATCGGGCATCTATTACGGGCATCGGGCATCCGGGCATGCGGGCATGTGCTCCGGGCATCTCGCGGGCATGCACGGGCATCGGGCATACGGGCATTGGAGAGCGGGCATCGGGCATAAATCGGGCATGGCGGGCATTGCGGGCATTAGCGGGCATTCTCGGGCATTTCGTGTACGGGCATTATACGGGCATGCGGGCATGGTCGGGCATAGGTAGGAGGGCCTTCGGGCATGGTTCGCGGGCATCGCGGGCATCCACCGGGCATTATGCGCGGGCATTGCGGGCATTACTCGGGCATACCGGGCATCCGGGCATCGTCGGGCATCGGGCATCGGGCATTCCGGGCATTAGTTCGACGGGCATGTTCGGGCATCGACGGGCATAGACGGGCATCGGGCATCGGGCATGTGTTACCGGGCATCGGGCATCCGGGCATCGCGGGCATCGGGCATCGGGCATCTCGGGCATGGCGGGCATGGCTAGGACCGGGCATCGGGCATGCGGGCATCGGGCATGCTAATCGGGCATCGGGCATCCCGGGCATCGGGCATCGGGCATCGGGCATTATCCCGGGCATTGAGATCGGGCATTAGTCCCCACCGGGCATGATCACTCTCTCGGGCATCGGGCATACGGGCATATCGGGCATCGGGCATCGGGCATAGTCGGGCATTTTCGGGCATGCGGGCATAGGTGGGTGCCGGGCATCGGGCATAGCCCGGGCATAATGCGGGCATCGACGGGCATTCCCGGGCATTCGGGCATGTTTCGGGCATCCCCGGGCATGCGCGGGCATCCGGGCATCACCTCGGGCATTTCGGGCATTCGGGCAT'
# motif = 'CGGGCATCG'
# for i in range(len(seq)):
#     if seq.startswith(motif,i):    #str.startswith(str, beg=0,end=len(string))  beg 和 end 为起始位置
#         print(i+1,end='\t')
#  使用正则查找
# import re
# pattern=re.compile(r'(?=ATAT)')    #（?=exp) 匹配exp(表达式）前面的位置
# for i in re.finditer(pattern,seq):
#     print(i.start()+1)

#斐波那契的兔子（计算每个月的兔子总对数，兔子有死亡）
# def f(n, k):
#     s = [0] * (k + 1)
#     s[0] = 1
#     for x in range(1, n):
#         s[1:k + 1] = s[0:k]
#         s[0] = sum(s[2:])
#     # print(s)
#     return sum(s[:-1])
#
# print(f(93,17))


#寻找一致序列  （共有序列：多条相同长度DNA字符串，对每个位置，选择出现最多的那个字符）

from collections import Counter
from collections import OrderedDict
with open(r'C:\Users\NB18040401\Desktop\prot.txt', 'wt') as f1:
    rosalind = OrderedDict()
    seqLength = 0
    with open(r'C:\Users\NB18040401\Desktop\rosalind_cons (1).txt') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                rosalindName = line
                rosalind[rosalindName] = ''
                # 跳出这个循环，进入下一个循环
                continue
                # 如果不是'>'开头，执行这一句
            rosalind[rosalindName] += line
            # len(ATCCAGCT)
            seqLength = len(rosalind[rosalindName])
        A, C, G, T = [], [], [], []
        consensusSeq = ''
        for i in range(seqLength):
            seq = ''
        # rosalind.keys = Rosalind_1...Rosalind_7
            for k in rosalind.keys():
                # 把 Rosalind_1...Rosalind_7 相同顺序的碱基加起来
                seq += rosalind[k][i]
            A.append(seq.count('A'))
            C.append(seq.count('C'))
            G.append(seq.count('G'))
            T.append(seq.count('T'))
        # 为seq计数
            print(seq)
            counts = Counter(seq)
            print(counts)
        # 从多到少返回,是个list啊，只返回第一个
            consensusSeq += counts.most_common()[0][0]
        f1.write(consensusSeq + '\n')
        f1.write('\n'.join(['A:\t' + '\t'.join(map(str, A)), 'C:\t' + '\t'.join(map(str, C)), 'G:\t' + '\t'.join(map(str, G)), 'T:\t' + '\t'.join(map(str, T))]))




