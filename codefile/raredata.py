import re

# with open('E:/Project/16S/nuohe/P180432-3/OTU/Diversity/arare_max69246/alpha_div_collated/shannon.txt') as f1:
#     with open('E:/Project/16S/nuohe/P180432-3/OTU/Diversity/arare_max69246/alpha_div_collated/shannon2.txt', 'w') as f2:
#         f2.write('sampleID\tGroup\tdepth\tobserved_otus\n')
#         colnames = f1.readline()
#         samplenames = colnames.strip('').split()[4:]
#         print(samplenames)
#         for line in f1:
#             line = line.strip().split()
#             depth = line[1]
#             observed_otus_list = line[3:]
#             for i, j in enumerate(samplenames):
#                 Group = re.search('[a-zA-Z]*', j).group()
#                 observed_otus = observed_otus_list[i]
#                 # f2.write(j + '\t' + Group + '\t' + depth + '\t' + observed_otus + '\n')


import pandas as pd
pd.set_option('display.max_columns', None)    # 设置显示所有列
pd.set_option('display.max_rows', None)      # 显示所有行

df = pd.read_csv('C:\\Users\\jbwang\\Desktop\\shannon.txt', index_col=1, sep='\t')
df = df.drop(['Unnamed: 0', 'iteration'], axis=1)   # axis=1 按列删除
df_group = df.groupby('sequences per sample')    # 分组
df_empty = pd.DataFrame(columns=['sampleID', 'shannon', 'Seqs', 'Group'])  # 创建空的dataframe
for i in df_group:
    newdf = i[1]
    newdf2 = newdf.mean().to_frame().reset_index()   # 求平均值
    newdf2['seqs'] = i[0]
    newdf2['group'] = newdf2['index'].str.extract('([a-zA-Z]*)')   # 正则提取
    newdf2.columns = ['sampleID', 'shannon', 'Seqs', 'Group']
    df_empty = df_empty.append(newdf2, ignore_index=True)  # 合并数据
    # pd.concat([df_empty, newdf2], ignore_index=True)
# print(df_empty)

df_empty.to_csv('C:\\Users\\jbwang\\Desktop\\shannon2.txt', sep='\t', index=False)