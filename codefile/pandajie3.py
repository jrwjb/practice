#从gbk文件中提取蛋白序列
import re
with open(r'C:\Users\NB18040401\Desktop\sequence.gb') as f1:
    with open(r'C:\Users\NB18040401\Desktop\protein.fa','w') as f2:
        s=f1.read()
        pattern1=re.compile(r'/protein_id="([\s\S]*?)"')
        pattern2=re.compile(r'/translation="([\s\S]*?)"')  #匹配多行内容

        s1=pattern1.findall(s)
        print(len(s1))
        s2=pattern2.findall(s)
        print(len(s2))
        l=[]
        for i in s2:
            l.append(i.replace(' ','').replace('\n',''))
        print(len(l))
        for i,j in zip(s1,l):
            f2.write('>'+i+'\n')
            f2.write(j+'\n')










