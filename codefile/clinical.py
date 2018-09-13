import pandas as pd

df = pd.read_excel('/Users/wjb/Desktop/常见实体瘤中英文对照.xlsx',sheet_name='Sheet1')
df = df['常见实体瘤中英文对照'].dropna()
df = df.str.lower()

#
# write_file = open('/Users/wjb/Desktop/clinical2.tsv','a')
#
#
# with open('/Users/wjb/Desktop/clinical_trails2.tsv') as f:
#     header = f.__next__()
#     write_file.write(header)
#     d={}
#     for index,line in enumerate(f):
#         d[index]=line
#     # 写入China行
#     for value in d.values():
#         s1 = value.split('\t')[21].strip('"')
#         s2 = value.split('\t')[26].strip('"')
#         if s1.lower() in df.values and s2 == 'China':
#             write_file.write(value)
#     #写入非China行
#     for value in d.values():
#         s1 = value.split('\t')[21].strip('"')
#         s2 = value.split('\t')[26].strip('"')
#         if s1.lower() in df.values and s2 != 'China':
#             write_file.write(value)
#
# write_file.close()


df_clinical = pd.read_table('/Users/wjb/Desktop/clinical_trails.tsv')
#目标字段小写
df_clinical.condition = df_clinical['condition'].str.lower()
#提取目标字段
df_clinical = df_clinical.loc[df_clinical['condition'].isin(df.values),:]
#提取China行
df_clinical_CN = df_clinical.loc[df_clinical['country'].isin(['China']),:]
#提取非China行
df_clinical_noCN = df_clinical.loc[~df_clinical['country'].isin(['China']),:]
#合并
df_combine = pd.concat([df_clinical_CN,df_clinical_noCN],join='outer')

df_combine.to_csv('/Users/wjb/Desktop/clinical2.csv',index=False)



