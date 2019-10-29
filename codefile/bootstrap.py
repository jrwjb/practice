import re
import xlrd
import numpy as np
import pandas as pd
from openpyxl import Workbook

def average(data):
    return np.mean(data)

def bootstrap(data, B, C, func, cal_type='experience'):
    '''
    :param data: array数组保存数据
    :param B: 抽样次数，通常 B >= 1000
    :param C: 置信水平
    :param func: 样本估计量
    :param cal_type: bootstrap 计算类型，经验法和百分位法，默认使用经验法
    :return: bootstrap 置信区间上下限
    '''
    array = np.array(data)
    n = len(array)
    result = []
    for _ in range(B):
        index_arr = np.random.randint(0, n, size=n)
        sample = array[index_arr]
        sample_result = func(sample)
        result.append(sample_result)

    if cal_type == 'experience':
        a = 1 - C
        k1 = int(B * a / 2)
        k2 = int(B * (1 - a / 2))
        result_sorted = sorted(result)
        lower = round(result_sorted[k1], 3)
        upper = round(result_sorted[k2], 3)
        return [lower, upper]
    else:
        lower_p = C / 2
        lower = max(0.0, np.percentile(result, lower_p))
        upper_p = (100 - C) + (C / 2)
        upper = min(1.0, np.percentile(result, upper_p))
        return f'[{lower}, {upper}]'

def process_data(file):
    df = pd.read_csv(file, sep='\t', index_col=0)
    normal_list = [i for i in df.columns if re.search('A', i)]
    df_normal = df[normal_list].T
    keep_list = ['Actinobacteria', 'Firmicutes', 'Bacteroidetes', 'Proteobacteria', 'Verrucomicrobia', 'Tenericutes', 'Patescibacteria']
    other_list = [i for i in df_normal.columns if i not in keep_list]
    df_keep = df_normal[keep_list]
    df_keep['Bacteroidetes/Firmicutes'] = df_keep['Bacteroidetes'] / df_keep['Firmicutes']
    df_keep['Others'] = df_normal[other_list].sum(axis=1)
    return df_keep

def sample_info(file):
    with open(file, encoding='utf8') as f:
        sample_info_dict = {line.strip().split('\t')[0]: line.strip().split('\t')[1] for line in f}
    return sample_info_dict

def write(data, sample, sample_dict, confidence_interval):
    '''
    :param data:  dataframe数据
    :param sample: 样本编号
    :param sample_dict: 样本编号对应的病人信息
    :param confidence_interval: 置信区间
    :return:
    '''
    model = xlrd.open_workbook('C:\\Users\\jbwang\\Desktop\\P20190700965-SX1\\model.xlsx').sheets()[0]
    wb = Workbook()
    ws = wb.active
    sample_name = sample_dict.get(sample)
    for row in range(model.nrows):
        line = model.row_values(row)
        if line[0] == '姓名':
            line[1] = sample_name
        elif line[0] == '样本类型':
            line[1] = '粪便'
        elif all([line[0] != '检测指标', line[0] != '']):
            tmp = line[0].split('(')[-1].strip(')')
            tmp_data = data.loc[sample, tmp]
            line[1] = tmp_data
            con_interval = confidence_interval.get(tmp)
            line[3] = f'{con_interval}'
            lower = float(con_interval[0])
            upper = float(con_interval[1])
            if tmp_data > upper:
                line[2] = '↑'
            elif tmp_data < lower:
                line[2] = '↓'
            else:
                line[2] = '-'
        ws.append(line)
    wb.save(f'C:\\Users\\jbwang\\Desktop\\P20190700965-SX1\\1\\{sample_name}.xlsx')

def main():
    data = process_data('C:\\Users\\jbwang\\Desktop\\P20190700965-SX1\\phylum.percent.xls')
    sample_dict = sample_info('C:\\Users\\jbwang\\Desktop\\P20190700965-SX1\\sample_info.txt')
    confidence_interval = {i: bootstrap(data[i], 1000, 0.90, average) for i in data.columns}
    for s in data.index:
        write(data, s, sample_dict, confidence_interval)

if __name__=='__main__':
    main()


