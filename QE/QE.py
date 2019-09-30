import os
import re
import time
import datetime
import sys
import glob
import xlrd
import uniprot_go
from uniprot_go import Spider
# import pandas as pd

def new_dir(qe_path):
    # lists = os.listdir(qe_path)
    # lists.sort(key=lambda fn: os.path.getctime(f'{qe_path}\\{fn}'))  #按时间排序
    for i in os.listdir(qe_path):
        newDir = os.path.join(qe_path, i)
        go_file = os.path.join(newDir, 'GO.xlsx')
        if not os.path.isfile(go_file):
            yield newDir

def ifExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write(path, file):
    ifExists(path)
    with open(path + '\\diff_list.txt', 'w') as diff:
        if file.endswith('xlsx'):
            data = xlrd.open_workbook(file)
            data_table = data.sheets()[0]

            c = 0
            for row in range(data_table.nrows):
                line = data_table.row_values(row)
                if str(line[0]).startswith('$') and str(line[0]).split('-')[1] == '1':
                    name = line[1].split('|')[1]
                    c += 1
                    diff.write(name + '\n')
            if c == 1:
                diff.write(name + '\n')

        elif file.endswith('csv'):
            data = open(file)
            c = 0
            for line in data:
                line = line.strip().split(',')
                if str(line[0]).startswith('$') and str(line[0]).split('-')[1] == '1':
                    name = line[1].split('|')[1]
                    c += 1
                    diff.write(name + '\n')
            if c == 1:
                diff.write(name + '\n')
            data.close()

def sub(file):
    if re.search(r'附件1', file):
        path = os.path.split(file)[0] + '\\' + file.split('\\')[-2]
        ifExists(path)
        data = data = xlrd.open_workbook(file)
        data_table = data.sheets()[0]
        with open(path + '\\diff_list.txt', 'w') as diff:
            c = 0
            for row in range(1, data_table.nrows):
                line = data_table.row_values(row)
                if not re.search('CON|REV', line[0]):
                    proteinID = line[1].split('|')[1]
                    c += 1
                    diff.write(proteinID + '\n')
            if c == 1:
                diff.write(proteinID + '\n')

    elif re.search(r'protein', file, re.I):
        path = os.path.split(file)[0] + '\\' + file.split('\\')[-2]
        ifExists(path)
        data = data = xlrd.open_workbook(file)
        data_table = data.sheets()[0]
        with open(path + '\\diff_list.txt', 'w') as diff:
            c = 0
            for row in range(1, data_table.nrows):
                line = data_table.row_values(row)
                tmp = str(line[0])
                c += 1
                diff.write(tmp + '\n')
            if c == 1:
                diff.write(tmp + '\n')


    else:
        path = re.sub(r'[（(|)）]', '', os.path.splitext(file)[0])
        if len(path.split('\\')[-1]) > 31:
            newpath = '\\'.join(path.split('\\')[:-1]) + '\\' + path.split('\\')[-1][:31]
            write(newpath, file)
        else:
            write(path, file)

def main():
    # qe = new_dir(qe_path)
    for qe in new_dir(qe_path):
        print(qe)
        for file in os.listdir(qe):
            file = qe + '\\' + file
            if os.path.isfile(file):
                sub(file)
        Spider(qe).main()
        # os.system(f'Rscript {path}\\R\\Uniprot_GO.R {qe}')

if __name__ == '__main__':
    try:
        path = sys.argv[0]
        path = '\\'.join(path.split('\\')[:-1])
        qe_path = os.path.join(path, 'Data')
        main()
    except Exception as ex:
        print(ex)
    finally:
        os.system('pause')
