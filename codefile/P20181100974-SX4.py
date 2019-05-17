import re
import json
import xlrd
import numpy as np
import pandas as pd
from openpyxl import Workbook

def kegg_anno(index):
    kegg = pd.read_excel('C:\\Users\\jbwang\\Desktop\\P20181100974-SX4\\kegg.xlsx', sheet_name=index)
    columns = ['Pathway_ID', 'level1', 'level2', 'Pathway', 'seqs_num']
    kegg_df = pd.DataFrame(columns=columns)
    kegg_df['Pathway_ID'] = kegg['Map_ID']
    kegg_df['Pathway'] = kegg['Map_Name']
    kegg_df['seqs_num'] = kegg['Seqs_Num']

    def ko_func(x):
        ko_list = []
        for p in x:
            p_id_list = p.split(';')
            ko = []
            for p_id in p_id_list:
                if p_id in ko_dict:
                    ko.append(ko_dict[p_id])
            ko_list.append(';'.join(ko))
        return ko_list


    def level():
        with open('C:\\Users\\jbwang\\Desktop\\kegg_level.json', 'r') as f:
            data = json.load(f)
            kegg_map = data['children']
            level1_list, level2_list = [], []
            for kegg_id in kegg['Map_ID']:
                for i in kegg_map:
                    A = i['name']
                    B_list = i['children']
                    for j in B_list:
                        B = j['name']
                        C_list = j['children']
                        for k in C_list:
                            C = k['name'].split()[0]
                            if C == kegg_id[3:]:
                                level1_list.append(A)
                                level2_list.append(B)
        return level1_list, level2_list

    if index == 1:
        # kegg_seqs = kegg['Seqs']
        # k_up_number = count_num(up_file[0], down_file[0], kegg_seqs)[0]
        # k_down_number = count_num(up_file[0], down_file[0], kegg_seqs)[1]
        # k_deg_number = np.array(k_up_number) + np.array(k_down_number)
        # k_up_data = count_num(up_file[0], down_file[0], kegg_seqs)[2]
        # k_down_data = count_num(up_file[0], down_file[0], kegg_seqs)[3]
        # kegg_df['Up_KO'] = ko_func(k_up_data)
        # kegg_df['Down_KO'] = ko_func(k_down_data)
        # kegg_df['Up_number'] = k_up_number
        # kegg_df['Down_number'] = k_down_number
        # kegg_df['DEG_number'] = k_deg_number
        # kegg_df['Up_gene'] = k_up_data
        # kegg_df['Down_gene'] = k_down_data
        kegg_df['level1'] = level()[0]
        kegg_df['level2'] = level()[1]
        # kegg_df['URL'] = kegg['URL']
    else:
        kegg_seqs = kegg['Test_Seq']
        k_up_number = count_num(up_file[0], down_file[0], kegg_seqs)[0]
        k_down_number = count_num(up_file[0], down_file[0], kegg_seqs)[1]
        k_deg_number = np.array(k_up_number) + np.array(k_down_number)
        k_up_data = count_num(up_file[0], down_file[0], kegg_seqs)[2]
        k_down_data = count_num(up_file[0], down_file[0], kegg_seqs)[3]
        kegg_df['Up_KO'] = ko_func(k_up_data)
        kegg_df['Down_KO'] = ko_func(k_down_data)
        kegg_df['Up_number'] = k_up_number
        kegg_df['Down_number'] = k_down_number
        kegg_df['DEG_number'] = k_deg_number
        kegg_df['Up_gene'] = k_up_data
        kegg_df['Down_gene'] = k_down_data
        kegg_df['level1'] = level()[0]
        kegg_df['level2'] = level()[1]
        kegg_df['Total_number'] = kegg['Ref']
        kegg_df['pvalue'] = kegg['P value']
        kegg_df['FDR'] = kegg['FDR']
    return kegg_df

# print(kegg_df.head())
# writer = pd.ExcelWriter(f'C:\\Users\\jbwang\\Desktop\\P20181100974-SX4\\kegg2.xlsx')
kegg_df1 = kegg_anno(1)
kegg_df1.to_csv('C:\\Users\\jbwang\\Desktop\\P20181100974-SX4\\1.csv', index=False)
# kegg_df2 = kegg_anno(2)
# kegg_df1.to_excel(writer, index=False, sheet_name='Annotation')
# kegg_df2.to_excel(writer, index=False, sheet_name='Enrichment')

# writer.save()
# writer.close()