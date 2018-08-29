import sys
import os
from collections import OrderedDict
import pandas as pd

#文件读写路径
read_path = '/Users/wjb/Desktop/Bed/'
write_path = '/Users/wjb/Desktop/NewBed/'

#重置columns、删除不要的行
ngs_file = pd.read_excel('/Users/wjb/Desktop/ngs.config.xlsx',sheet_name = '项目和基因对应表')
ngs_file.columns = ngs_file.iloc[0]
ngs_file = ngs_file.drop([0])

#按panel对数据分组
ngs_file_panel = ngs_file.groupby('上机sample sheet项目描述')

#获取目标小panel及对应的基因名称
#panel_read='QIAGEN-CRC18'
panel_read = sys.argv[1].split('.')[0]
def get_panel(panel_read):
    dict_panel = OrderedDict()
    for panel in ngs_file_panel:
        if panel[0] == panel_read:
            df = panel[1][['基因名称(逗号隔开)','项目简称']].drop_duplicates()
            list_project = list(df['项目简称'])
            list_genename = list(df['基因名称(逗号隔开)'])
            for i,j in zip(list_project,list_genename):
                dict_panel[i] = j
    return dict_panel


#获取大panel
# f_panel=open('/Users/wjb/Desktop/Bed/QIAGEN-CRC18.bed')
f_panel = open(read_path+sys.argv[1])
bed_list = []
for i in f_panel:
    if i.split()[-1] != '-':
        for k,v in get_panel(panel_read).items():
            gene_name = v.split(',')
            for gene in gene_name:
                if gene in i.split()[-1]:
                    s = '\t'.join(['\t'.join(i.split()[:-1]),gene,i.split()[-1],k])
                    bed_list.append(s)


#写入文件
write_file_list = [write_path + k + '.bed' for k in get_panel(panel_read)]

for k,j in zip(get_panel(panel_read).keys(),write_file_list):
    f_write = open(j,'w')
    for i in bed_list:
        if i.split()[-1] == k == j.split('/')[-1].split('.')[0]:
            f_write.write('\t'.join(i.split()[:4])+'\n')

    f_write.close()


f_panel.close()

