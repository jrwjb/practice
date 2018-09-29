import re
import xlrd
import pandas as pd
from openpyxl import Workbook

class R_W_file(object):

    def __init__(self,data,gene_info,NM,drugs,middleFile):
        self._data = data
        self._gene_info = gene_info
        self._NM = NM
        self._drugs = drugs
        self._middleFile = middleFile

    def read_file(self):
        return xlrd.open_workbook(self._data).sheet_by_index(0)

    def gene_info(self):
        gene_info_df = pd.read_excel(self._gene_info,sheet_name='52基因解释')
        gene_info_dict = {}
        for i, j in zip(gene_info_df['gene'], gene_info_df['背景']):
            gene_info_dict[i] = j

        return gene_info_dict

    def NM(self):
        NM_df = pd.read_excel(self._NM,sheet_name='Sheet1')
        df1 = NM_df.iloc[:, [0, 1]]
        df2 = NM_df.iloc[:, [3, 4]].dropna()
        df3 = NM_df.iloc[:, [6, 7]].dropna()
        NM_dict = {}
        def get_NM(x, y):
            for i, j in zip(x, y):
                NM_dict[i] = j
        get_NM(df1['靶向药物（32基因）'], df1['refGene NM'])
        get_NM(df2['肺癌18'], df2['refGene NM.1'])
        get_NM(df3['结直肠癌-新'], df3['refGene NM.2'])

        return NM_dict

    def drugs(self):
        drugs = xlrd.open_workbook(self._drugs)
        drugs_table = drugs.sheet_by_index(0)
        drugs_list, drug_type_list, level = [], [], []
        for row in range(2, drugs_table.nrows):
            gene = drugs_table.row_values(row)[4]
            if gene == gene_name:
                drugs_list.append(drugs_table.row_values(row)[10])
                drug_type_list.append(drugs_table.row_values(row)[9])
                level.append(str(drugs_table.row_values(row)[7]))

        s_drug = '/'.join(set(drugs_list))
        s_type = '/'.join(set(drug_type_list))
        s_level = '/'.join(set(level))

        return s_drug,s_type,s_level

    def ref_dict1(self):
        d_aa = {
                'A': 'Ala', 'C': 'Cys', 'D': 'Asp', 'E': 'Glu', 'F': 'Phe', 'G': 'Gly', 'H': 'His', 'I': 'Ile', 'K': 'Lys',
                'L': 'Leu', 'M': 'Met', 'N': 'Asn', 'P': 'Pro', 'Q': 'Gln', 'R': 'Arg', 'S': 'Ser', 'T': 'Thr', 'V': 'Val',
                'W': 'Trp', 'Y': 'Tyr'
                }
        return d_aa

    def ref_dict2(self):
        d_aa_cn = {
                    'A': '丙氨酸', 'C': '半胱氨酸', 'D': '天冬氨酸', 'E': '谷氨酸', 'F': '苯丙氨酸', 'G': '甘氨酸', 'H': '组氨酸',
                    'I': '异亮氨酸', 'K': '赖氨酸', 'L': '亮氨酸', 'M': '甲硫氨酸', 'N': '天冬酰胺', 'P': '脯氨酸', 'Q': '谷氨酰胺',
                    'R': '精氨酸', 'S': '丝氨酸', 'T': '苏氨酸', 'V': '缬氨酸', 'W': '色氨酸', 'Y': '酪氨酸'
                    }
        return d_aa_cn

    def write(self):
        wb = Workbook()
        ws = wb.active

        data_table = self.read_file()
        gene_info_d = self.gene_info()
        NM_d = self.NM()
        aa = self.ref_dict1()
        aa_cn = self.ref_dict2()

        ws.append(data_table.row_values(0) + ['hgvs', 'gene_var', 'gene_info','drugs','cancer_type','drug_level'])

        for row in range(1, data_table.nrows):
            line = data_table.row_values(row)
            AA = data_table.row_values(row)[15]
            filter = data_table.row_values(row)[9]
            if AA != '.' and not re.search(r'.*5%.*',filter):
                NM_list = AA.split(',')
                for i in NM_list:
                    global gene_name
                    gene_name = i.split(':')[0]
                    NM = i.split(':')[1]
                    if gene_name in NM_d.keys() and NM == NM_d[gene_name]:
                        p = i.split(':')[-1].split('.')[1]
                        if re.search(r'^[A-Z]\d+[A-Z]', i.split(':')[3].split('.')[1]):
                            c = i.split(':')[3].split('.')[1]
                            hgvs = '{}:{}:{}:c.{}{}>{}:p.{}{}{}'.format(gene_name, NM, i.split(':')[2], c[1:-1], c[0],
                                                                        c[-1], aa[p[0]], p[1:-1], aa[p[-1]])
                            line.append(hgvs)
                            gene_var = '{}基因{}第{}位密码子{}置换为{}使得第{}位氨基酸由{}变成了{},此变异在样本中的频率位{}'.format(
                                gene_name,
                                i.split(':')[2],
                                c[1:-1], c[0],
                                c[-1], p[1:-1],
                                aa_cn[p[0]],
                                aa_cn[p[-1]],
                                data_table.row_values(row)[8])
                            line.append(gene_var)
                            if gene_name in gene_info_d:
                                gene_info = gene_info_d[gene_name]
                                line.append(gene_info)
                            line.append(self.drugs()[0])
                            line.append(self.drugs()[1])
                            line.append(self.drugs()[2])
                            ws.append(line)

                        elif re.search(r'.*del.*', i.split(':')[3].split('.')[1]):
                            line.append(i)
                            line.append('请报告审核者根据hgvs命名提供')
                            gene_info = gene_info_d[gene_name]
                            line.append(gene_info)
                            line.append(self.drugs()[0])
                            line.append(self.drugs()[1])
                            line.append(self.drugs()[2])
                            ws.append(line)

                        else:
                            line.append(i)
                            line.append('请报告审核者根据hgvs命名提供')
                            gene_info = gene_info_d[gene_name]
                            line.append(gene_info)
                            line.append(self.drugs()[0])
                            line.append(self.drugs()[1])
                            line.append(self.drugs()[2])
                            ws.append(line)

        wb.save(self._middleFile)

class TargetApi(object):
    def __init__(self,data,api):
        self._data = data
        self._api = api

    def api(self):
        targetApi = pd.read_excel(self._api, sheet_name='Worksheet')
        df_api = pd.DataFrame(columns=targetApi.columns)
        df_zn = (pd.DataFrame(targetApi.iloc[0, :])).T
        df_data = pd.read_excel(self._data, sheet_name='Sheet')

        d = {''.join(re.split('[_.]', i)).lower(): df_data[i] for i in df_data.columns}

        for i in df_api.columns:
            if i.lower() in d:
                df_api[i] = d[i.lower()]

        df_api.sampleSn = df_data['SampleID'].str[3:-2]
        df_api.geneName = pd.Series([i.split(':')[0] for i in df_data['hgvs']])
        df_api.wxz = pd.Series([i.split(':')[2] for i in df_data['hgvs']])
        df_api.zlb = pd.Series([i.split(':')[1] for i in df_data['hgvs']])
        df_api.hgsGb = pd.Series([i.split(':')[3] for i in df_data['hgvs']])
        df_api.ajsGb = pd.Series([i.split(':')[4] for i in df_data['hgvs']])
        df_api.posStart = df_data['Start']
        df_api.posEnd = df_data['End']

        df = pd.concat([df_zn, df_api])

        df.to_excel('/Users/wjb/Desktop/result/targetApiTest.xlsx', index=False)


class HeredityApi(object):
    def __init__(self,data,gene_info,api):
        self._data = data
        self._gene_info = gene_info
        self._api = api

    def gene_info(self):
        gene_dict = {}
        gene_table = xlrd.open_workbook(self._gene_info).sheet_by_index(1)
        for row in range(1,gene_table.nrows):
            line = gene_table.row_values(row)
            gene_dict[line[0]] = line[1:]

        return gene_dict

    def api(self):
        api_table = xlrd.open_workbook(self._api).sheet_by_index(0)
        data_table = xlrd.open_workbook(self._data).sheet_by_index(0)

        wb = Workbook()
        ws = wb.active

        ws.append(api_table.row_values(0))
        ws.append(api_table.row_values(1))

        for row in range(1,data_table.nrows):
            line = data_table.row_values(row)
            temp = []
            sample_barcode = line[2][:-2] + ','
            if line[15].split(':')[0] in self.gene_info():
                temp.extend(sample_barcode.split(','))
                temp.extend(self.gene_info()[line[15].split(':')[0]])
                ws.append(temp)


        wb.save('/Users/wjb/Desktop/result/heredityApiTest.xlsx')


if __name__=='__main__':
    data = '/Users/wjb/Desktop/result/data.xls'
    gene_info = '/Users/wjb/Desktop/result/NGS报告改版-知识库-基因介绍.xlsx'
    NM = '/Users/wjb/Desktop/result/NM.xlsx'
    drugs = '/Users/wjb/Desktop/result/靶向用药自动关联.xlsx'
    middleFile = '/Users/wjb/Desktop/result/target.xlsx'
    r_w_file = R_W_file(data,gene_info,NM,drugs,middleFile)
    r_w_file.write()
    api_1 = '/Users/wjb/Desktop/result/靶向结果API.xlsx'
    resultApi = TargetApi(middleFile,api_1)
    resultApi.api()
    api_2 = '/Users/wjb/Desktop/result/遗传API.xlsx'
    heredityApi = HeredityApi(middleFile,gene_info,api_2)
    heredityApi.api()




