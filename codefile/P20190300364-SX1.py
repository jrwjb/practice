import re
import os
import xlrd
import time
import numpy as np
import pandas as pd
# from tqdm import tqdm
from functools import wraps
from openpyxl import Workbook

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)    # 设置显示所有列
pd.set_option('display.max_rows', None)      # 显示所有行

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
            (function.__name__, str(t1-t0))
            )
        return result
    return function_timer

def get_file(path):
    if os.path.exists(f'{path}/报告及附件'):
        os.system(f'rm -rf {path}/报告及附件')
    for file in os.listdir(path):
        file = f'{path}/{file}'
        if os.path.isdir(file):
            yield file

# def proteinName(path):
#     df = pd.read_excel(f'{path}/附件1_修饰肽段鉴定列表.xlsx', sheet_name=0)
#     df2 = df.drop_duplicates(['Protein'])
#     d = {i: j for i, j in zip(df2['Protein'], df2['Protein Name'])}
#     return d

def add_ProteinName(x):
    return ';'.join([f'{i}|{d.get(i)}' for i in re.split('[ |,]', x)])

@fn_timer
def GO(file):
    group = file.split('/')[-1]
    newfile = f'{path}/报告及附件/{group}/go'
    os.system(f'mkdir -p {newfile}')
    os.system(f'cp {file}/go/*.txt {newfile}')
    # print(f'{file}/go/GO.xlsx')
    go = pd.read_excel(f'{file}/go/GO.xlsx', None)
    # 写入多个sheet
    # print(f'{newfile}/GO.xlsx')
    writer = pd.ExcelWriter(f'{newfile}/go.xlsx')
    for k in go.keys():
    # for k in tqdm(list(data.keys())):
        if k == 'Enrichment':
            df = go[k]
            df['TestSeqs'] = df['TestSeqs'].apply(add_ProteinName)
            df.to_excel(writer, sheet_name=k, index=False)
        else:
            df = go[k]
            df['Sequences\n'] = df['Sequences\n'].apply(add_ProteinName)
            df.to_excel(writer, sheet_name=k, index=False)

    writer.save()
    writer.close()

@fn_timer
def kegg(file):
    group = file.split('/')[-1]
    newfile = f'{path}/报告及附件/{group}/kegg'
    os.system(f'mkdir -p {newfile}')
    os.system(f'cp {file}/kegg/*.txt {newfile}')
    # print(f'{file}/kegg/kegg.xlsx')
    data = pd.read_excel(f'{file}/kegg/kegg.xlsx', None)
    # 写入多个sheet
    # print(f'{newfile}/kegg.xlsx')
    writer = pd.ExcelWriter(f'{newfile}/kegg.xlsx')
    for k in data.keys():
        if k == 'Enrichment':
            df = data[k]
            df['Test_Seq'] = df['Test_Seq'].apply(add_ProteinName)
            df.to_excel(writer, sheet_name=k, index=False)
        else:
            df = data[k]
            df.to_excel(writer, sheet_name=k, index=False)

    writer.save()
    writer.close()

@fn_timer
def cluster(file, data2):
    group = file.split('/')[-1]
    newfile = f'{path}/报告及附件/{group}/cluster'
    os.system(f'mkdir -p {newfile}')
    data = pd.read_csv(f'{file}/CLUSTER/cluster.txt', sep='\t')
    data.columns = [i.lower() if i =='ID' else i for i in data.columns]
    data['id'] = data['id'].apply(lambda x : f"{x.split('|')[0]}|{d.get(x.split('|')[0])}|{x.split('|')[1]}")
    data.to_csv(f'{newfile}/cluster.txt', index=False, sep='\t')
  
    for k in data2.keys():
        if '有无' in k and group in k:
            df1 = data2[k].iloc[:,[0,1,12]]
            df1 = df1['Protein'].str.cat([df1['Protein Name'], df1['Sequence window']], sep='|').to_frame()
            df1.columns = ['id']
            df2 = data2[k].iloc[:,-6:].fillna(0)
            df2.columns = [x.replace('Intensity ', '') for x in df2.columns]
            # df2 = df2.apply(lambda x:(x - np.mean(x)) / np.std(x, ddof=1), axis=1)  ### z-score标准化 ddof=1 为求样本方差， ddof=0 为求整体方差
            df2 = df2.apply(lambda x: np.log2(x + 1))
            df = pd.concat([df1, df2], axis=1)
            df.to_csv(f'{newfile}/cluster_YN.txt', index=False, sep='\t')


@fn_timer
def main(path):
    for file in get_file(path):
        # print(file)
        GO(file)
        kegg(file)
        cluster(file, data2)

@fn_timer
def write2():
    x = 'P01902,Q61160,P16858,P27870,P42230,Q64735,O54885'
    print(add_ProteinName(x))
    # print(proteinName())

if __name__=='__main__':
    path = '/home/apt/Desktop/P20190300364-SX1'
    df = pd.read_excel(f'{path}/附件1_修饰肽段鉴定列表.xlsx', sheet_name=0)
    df2 = df.drop_duplicates(['Protein'])
    d = {i: j for i, j in zip(df2['Protein'], df2['Protein Name'])}
    data2 = pd.read_excel(f'{path}/附件2_修饰肽段显著性差异分析列表.xlsx', None)
    main(path)





