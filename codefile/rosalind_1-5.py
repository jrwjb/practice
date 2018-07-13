#碱基计数
# from collections import Counter
# with open(r'C:\Users\NB18040401\Desktop\rosalind_dna.txt') as f1:
#     c=Counter()
#     for i in f1.read():
#         c[i]+=1
#     print(c)

#使用字典计数  之  碱基计数
# count={}
# for i in f1.read():
#     count.setdefault(i,0)
#     count[i]+=1
# print(count)

#DNA变RNA
# import re
# # dna= 'GATGGAACTTGACTACGTAAATT'
# with open(r'C:\Users\NB18040401\Desktop\rosalind_rna.txt') as f1:
#     pattern=re.compile(r'T')
#     rna=pattern.sub('U',f1.read())
#     print(rna)

#DNA反向互补链
# # dna="AAAACCCGGT"
# with open(r'C:\Users\NB18040401\Desktop\rosalind_revc.txt') as f1:
#     dna=f1.read().strip()
#     d={'A':'T','G':'C','C':'G','T':'A'}
#     dna_rev=dna[::-1]
#     for i in dna_rev:
#         print(d[i],end='')

#斐波那契的兔子
# def fib(n,k):
#     if n<=2:
#         return (1)
#     else:
#         return (fib(n-1,k)+fib(n-2,k)*k)
# print(fib(34,4))

#从fasta文件中提取指定序列

# with open(r'C:\Users\NB18040401\Desktop\rosalind_revc.txt') as f1:
#     name='Rosalind_0808'                              #序列ID
#     flag=0                                            #设置变量，1 打印 0 不打印
#     for line in f1:
#         line=line.strip()
#         if line[0] == '>':
#             if line.split()[0][1:] == name:
#                 flag = 1
#                 print(line)                           #打印指定序列的名字
#             else:
#                 flag = 0
#         else:
#             if flag == 0:
#                 pass
#             else:
#                 print(line)                           #打印指定的序列




#计算GC含量

# with open(r'C:\Users\NB18040401\Desktop\rosalind_gc.txt') as f1:
#     # with open(r'C:\Users\NB18040401\Desktop\txt.txt','w') as f2:
#     d = {}
#     for line in f1:
#         line=line.strip()
#         if line.startswith('>'):
#             name=line
#             d[name]=''                  #序列名放入字典作为 key
#             # continue
#         else:
#             d[name]+=line.upper()       #序列放入字典作为 value
#     # f2.write(str(d))
#     c = []
#     for i in d.values():
#         # print(i,end='\n')
#         c.append(((i.count('G')+i.count('C'))/len(i))*100)
#     print(c)
#     print(max(c))


#计算GC含量（其他方法）
# from operator import itemgetter
# from collections import OrderedDict
# seq=OrderedDict()                  #定义有序字典
# with open(r'C:\Users\NB18040401\Desktop\rosalind_gc.txt') as f:
#     for line in f:
#         line=line.strip()
#         if line.startswith('>'):
#             name=line[1:]
#             seq[name]=''
#             continue                      #结束本次循环进入下次循环
#         seq[name]+=line.upper()
#     # print(seq)
#     c = []
#     for i in seq.values():
#         c.append(((i.count('G')+i.count('C'))/len(i))*100)
#     print(max(c))





