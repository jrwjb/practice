#统计文本中的每个单词出现次数并排序
import re
with open(r'C:\Users\wjb\Desktop\1\1.txt',encoding='utf-8') as f1:
    txt=f1.read()
    s=re.sub(r'[,;."‘“]','',txt).split()
    for i in sorted(set(s)):
        print('{}\t=>\t{}'.format(i,s.count(i)))
