import re
import json
import xlrd
import time
import numpy as np
import pandas as pd
from openpyxl import Workbook
from functools import wraps

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
    with open('E:\\Project\\Protein\\QE\R20190300409\\id.txt') as f:
        for i in f:
            protein = i.split('|')[1]
            if re.search('GN=\S+', i):
                gene = re.search('GN=\S+', i).group().split('=')[1]
            else:
                gene = ''
            gene_dict[protein] = gene
            # f2.write(f'{protein},{gene}\n')
    return gene_dict

# go = pd.read_excel('E:\\Project\\Protein\\QE\R20190300409\\GO.xlsx')
@fn_timer
def write():
    go = xlrd.open_workbook('E:\\Project\\Protein\\QE\R20190300409\\GO.xlsx')
    go_table = go.sheet_by_index(8)

    wb = Workbook()
    ws = wb.active
    ws.append(go_table.row_values(0) + ['GeneName'])
    # ws.append(go_table.row_values(1))

    for row in range(1, go_table.nrows):
        line = go_table.row_values(row)
        proteinID = line[0]
        # # print(proteinID)
        geneName = gene_name().get(proteinID)
        print(geneName)
        # line.append(geneName)
        # ws.append(line)

    wb.save('E:\\Project\\Protein\\QE\R20190300409\\GO2.xlsx')


if __name__ == '__main__':
    write()
