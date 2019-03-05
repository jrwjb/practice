import os
import re
import time
import datetime
import sys
import glob
import xlrd
import pandas as pd

def new_dir(qe_path):
    lists = os.listdir(qe_path)
    lists.sort(key=lambda fn: os.path.getctime(f'{qe_path}/{fn}'))  #按时间排序
    newDir = os.path.join(qe_path, lists[-1])
    return newDir

def get_file(data):
    # file_list = []
    for file in glob.glob(data + '/*.xlsx'):
        yield file
        # file_list.append(file)
    # return file_list

def ifExists(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def write(path, file):
    ifExists(path)
    with open(path + '/diff_list.txt', 'w') as diff:
        data = xlrd.open_workbook(file)
        data_table = data.sheets()[0]

        for row in range(data_table.nrows):
            line = data_table.row_values(row)
            if str(line[0]).startswith('$') and str(line[0]).split('-')[1] == '1':
                name = line[1].split('|')[1]
                diff.write(name + '\n')

def sub(file):
    if re.search(r'附件1', file):
        path = '/'.join(file.split('/')[0:-1]) + '/' + file.split('/')[-2]
        # print(path)
        ifExists(path)
        df = pd.read_excel(file, sheet_name='proteinGroups')
        df = df[~df['Protein IDs'].str.contains('CON|REF', regex=True)]  # ~取反符号，通过取反筛选掉特定行
        new_df = df['Fasta headers'].str.split('|', expand=True).iloc[:, 1].to_frame()
        new_df.to_csv(path + '/diff_list.txt', index=False, header=False)

    elif re.search(r'protein', file):
        path = file.split('_')[0]
        ifExists(path)
        df = pd.read_excel(file, sheet_name='Sheet1')
        new_df = df['Accession'].to_frame()
        new_df.to_csv(path + '/diff_list.txt', index=False, header=False)

    else:
        path = re.sub(r'[（|）]', '', file.split('.')[0])
        if len(path.split('/')[-1]) > 31:
            newpath = '/'.join(path.split('/')[:-1]) + '/' + path.split('/')[-1][:31]
            # print(len(path.split('/')[-1]))
            write(newpath, file)
        else:
            write(path, file)

def main():
    qe = new_dir(qe_path)
    # qe = newtime(qe_path)
    print(qe)
    # file_list = []
    for file in get_file(qe):
        # file_list.append(re.split('[/.]', file)[-2])
        if re.search(r'GO', file):
            break
        else:
            sub(file)
    # if 'GO' in file_list:
    #     pass
    # else:
    os.system('Rscript /home/apt/e/Script/R/Uniprot_GO.R {}'.format(qe))

if __name__ == '__main__':
    # qe = sys.argv[1]
    qe_path = '/home/apt/Project/Protein/QE'
    main()

    # os.system('Rscript /home/apt/e/Script/R/Uniprot_GO.R {}'.format(qe))