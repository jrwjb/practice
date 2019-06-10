import re
import sys
import json
import xlrd
import time
import numpy as np
import pandas as pd
from openpyxl import Workbook
from functools import wraps
from tqdm import tqdm

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

def gene_name():
    gene_dict = {}
    # protein_list, gene_list = [], []
    with open('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\id.txt') as f:
        for i in f:
            protein = i.split('|')[1]
            # protein_list.append(protein)
            if re.search('GN=\S+', i):
                gene = re.search('GN=\S+', i).group().split('=')[1]
            else:
                gene = ''
            gene_dict[protein] = gene
            # gene_list.append(gene)
            # f2.write(f'{protein},{gene}\n')

    return gene_dict

# @fn_timer
def write():
    go = xlrd.open_workbook('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO.xlsx')
    go_table = go.sheet_by_index(0)

    wb = Workbook()
    ws = wb.active
    ws.append(go_table.row_values(0) + ['GeneName'])
    # ws.append(go_table.row_values(1))

    # for row in range(1, go_table.nrows):
    for row in tqdm(range(1, go_table.nrows)):    #### 使用进度条展示
        line = go_table.row_values(row)
        proteinID = line[0]
        # # print(proteinID)
        geneName = gene_name().get(proteinID)
        # print(geneName)
        line.append(geneName)
        ws.append(line)



    wb.save('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO2.xlsx')

@fn_timer
def write2():
    ## 字典构建dataframe
    df = pd.DataFrame.from_dict(gene_name(), orient='index')
    df.columns = ['GeneName']
    go = pd.read_excel('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO.xlsx', None, index_col=0)
    # 写入多个sheet
    writer = pd.ExcelWriter('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\报告及附件\\GO.xlsx')
    # print(go.keys())
    # for k in go.keys():
    for k in tqdm(list(go.keys())):     ## 添加进度条
        data = go[k]
        #直接使用join
        new_df = data.join(df)
        newcol = ['GeneName']
        newcol.extend(data.columns.tolist())
        new_df = new_df[newcol]
        # new_df.to_excel('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO3.xlsx')
        new_df.to_excel(writer, sheet_name=k)

    writer.save()
    writer.close()


    #########先按蛋白筛选基因名
    # gene_df = df.loc[go.index]
    # ##concat方法
    # # new_df = pd.concat([gene_df, go], sort=False, axis=1)
    # # new_df.to_excel('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO3.xlsx')
    # # # print()
    # # ## join方法
    # new_df = gene_df.join(go)
    # new_df.to_excel('C:\\Users\\jbwang\\Desktop\\R20190500644-SX1\\GO3.xlsx')
    # # print()

if __name__ == '__main__':
    # write()
    write2()


