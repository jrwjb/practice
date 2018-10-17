import re
import xlrd
import pandas as pd

#定义读写文件的类，用以生成中间文件
class R_W_file(object):

    def __init__(self,data,gene_info,NM,drugs,middleFile):
        self._data = data
        self._gene_info = gene_info
        self._NM = NM
        self._drugs = drugs
        self._middleFile = middleFile

    #参考基因描述
    def gene_info(self):
        gene_info_df = pd.read_excel(self._gene_info,sheet_name='52基因解释')
        gene_info_dict = {}
        for i, j in zip(gene_info_df['gene'], gene_info_df['背景']):
            gene_info_dict[i] = j

        return gene_info_dict

    #参考转录本
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

    #参考靶向药
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

    #氨基酸中英文及简写
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
        with open(self._data) as f:
            with open(self._middleFile,'w',encoding='gbk') as fw:

                gene_info_d = self.gene_info()
                NM_d = self.NM()
                aa = self.ref_dict1()
                aa_cn = self.ref_dict2()

                title = f.__next__()
                add_title = ['.','.','vcf_chr','vcf_pos','vcf_id','vcf_ref','vcf_alt','vcf_qual','vcf_filter','vcf_info','vcf_format','vcf_format_val','hgvs', 'gene_var', 'gene_info','drugs','cancer_type','drug_level']
                new_title = title.strip() + '\t' + '\t'.join(add_title)
                #print(new_title)
                fw.write(new_title + '\n')

                for line in f:
                    line_list = line.strip().split('\t')
                    filter_freq = line_list[11]
                    if filter_freq == '.' or float(filter_freq) <= 0.05:
                        filter_funcRefGene = line_list[5]
                        funcRefGene_1 = ['intergenic','updtream','ncRNA_exonic']
                        if filter_funcRefGene not in funcRefGene_1:
                            funcRefGene_2 = ['UTR3','UTR5','intronic']
                            exonic = line_list[8]
                            exonic_pattern = re.compile(r'synonymous')
                            clinsig = line_list[22]
                            clinsig_pattern_1 = re.compile(r'[benign|.]',re.I)
                            clinsig_pattern_2 = re.compile(r'benign', re.I)
                            if filter_funcRefGene in funcRefGene_2 and clinsig_pattern_1.search(clinsig):
                                continue
                            elif exonic_pattern.match(exonic) and clinsig_pattern_2.search(clinsig):
                                continue
                            else:

                                AA = line_list[9]
                                freq = float(line_list[-1].split(':')[1].split(',')[-1]) / (
                                            float(line_list[-1].split(':')[1].split(',')[-1]) + float(
                                        line_list[-1].split(':')[1].split(',')[0]))
                                if AA != '.':
                                    NM_list = AA.split(',')

                                    global gene_name
                                    gene_name = NM_list[0].split(':')[0].strip('"')
                                    #print(gene_name)
                                    if gene_name in NM_d.keys():
                                        for i in NM_list:
                                            NM = i.split(':')[1]
                                            if NM == NM_d[gene_name]:
                                                p = i.split(':')[-1].split('.')[1]
                                                if re.search(r'^[A-Z]\d+[A-Z]', i.split(':')[3].split('.')[1]):
                                                    c = i.split(':')[3].split('.')[1]

                                                    # AAreferenceChanges更改为标准hgvs命名
                                                    hgvs = '{}:{}:{}:c.{}{}>{}:p.{}{}{}'.format(gene_name, NM,
                                                                                                i.split(':')[2], c[1:-1],
                                                                                                c[0],c[-1], aa[p[0]],
                                                                                                p[1:-1],aa[p[-1]])
                                                    line_list.append(hgvs)
                                                    gene_var = '{}基因{}第{}位密码子{}置换为{}使得第{}位氨基酸由{}变成了{},此变异在样本中的频率为{}'.format(
                                                        gene_name,
                                                        i.split(':')[2],
                                                        c[1:-1], c[0],
                                                        c[-1], p[1:-1],
                                                        aa_cn[p[0]],
                                                        aa_cn[p[-1]],
                                                        str(freq)[0:6])
                                                    line_list.append(gene_var)
                                                    if gene_name in gene_info_d:
                                                        gene_info = gene_info_d[gene_name]
                                                        line_list.append(gene_info)
                                                    line_list.append(self.drugs()[0])
                                                    line_list.append(self.drugs()[1])
                                                    line_list.append(self.drugs()[2])
                                                    s = '\t'.join(line_list)
                                                    #print(s)
                                                    fw.write(s+'\n')

                                                elif re.search(r'.*del.*', i.split(':')[3].split('.')[1]):
                                                    line_list.append(i)
                                                    line_list.append('请报告审核者根据hgvs命名提供')
                                                    if gene_name in gene_info_d:
                                                        gene_info = gene_info_d[gene_name]
                                                        line_list.append(gene_info)
                                                    line_list.append(self.drugs()[0])
                                                    line_list.append(self.drugs()[1])
                                                    line_list.append(self.drugs()[2])
                                                    s = '\t'.join(line_list)
                                                    # print(s)
                                                    fw.write(s + '\n')

                                                else:
                                                    line_list.append(i)
                                                    line_list.append('请报告审核者根据hgvs命名提供')
                                                    if gene_name in gene_info_d:
                                                        gene_info = gene_info_d[gene_name]
                                                        line_list.append(gene_info)
                                                    line_list.append(self.drugs()[0])
                                                    line_list.append(self.drugs()[1])
                                                    line_list.append(self.drugs()[2])
                                                    s = '\t'.join(line_list)
                                                    # print(s)
                                                    fw.write(s + '\n')

                                    else:
                                        if len(AA.split(',')) == 1:
                                            #print(AA)
                                            if not re.search(r'.*del.*',AA):
                                                hgvs = '{}:c.{}{}>{}:p.{}{}{}'.format(':'.join(AA.split(':')[:3]),
                                                                                      AA.split(':')[3].split('.')[-1][1:-1],
                                                                                      AA.split(':')[3].split('.')[-1][0],
                                                                                      AA.split(':')[3].split('.')[-1][-1],
                                                                                      aa[AA.split(':')[-1].split('.')[-1][0]],
                                                                                      AA.split(':')[-1].split('.')[-1][1:-1],
                                                                                      aa[AA.split(':')[-1].split('.')[-1][-1]])
                                                line_list.append(hgvs)
                                                gene_var = '{}基因{}第{}位密码子{}置换为{}使得第{}位氨基酸由{}变成了{},此变异在样本中的频率为{}'.format(
                                                    AA.split(':')[0],
                                                    AA.split(':')[2],
                                                    AA.split(':')[3].split('.')[-1][1:-1],
                                                    AA.split(':')[3].split('.')[-1][0],
                                                    AA.split(':')[3].split('.')[-1][-1],
                                                    AA.split(':')[-1].split('.')[-1][1:-1],
                                                    aa_cn[AA.split(':')[-1].split('.')[-1][0]],
                                                    aa_cn[AA.split(':')[-1].split('.')[-1][-1]],
                                                    str(freq)[0:6])
                                                line_list.append(gene_var)
                                                s = '\t'.join(line_list)
                                                # print(s)
                                                fw.write(s + '\n')

                                            else:
                                                line_list.append(AA)
                                                line_list.append('请报告审核者根据hgvs命名提供')
                                                s = '\t'.join(line_list)
                                                # print(s)
                                                fw.write(s + '\n')
                                        else:
                                            AA2 = AA.split(',')[0].strip('"')

                                            if not re.search(r'.*del.*', AA2):
                                                hgvs = '{}:c.{}{}>{}:p.{}{}{}'.format(':'.join(AA2.split(':')[:3]),
                                                                                      AA2.split(':')[3].split('.')[-1][
                                                                                      1:-1],
                                                                                      AA2.split(':')[3].split('.')[-1][
                                                                                          0],
                                                                                      AA2.split(':')[3].split('.')[-1][
                                                                                          -1],
                                                                                      aa[AA2.split(':')[-1].split('.')[
                                                                                          -1][0]],
                                                                                      AA2.split(':')[-1].split('.')[-1][
                                                                                      1:-1],
                                                                                      aa[AA2.split(':')[-1].split('.')[
                                                                                          -1][-1]])
                                                line_list.append(hgvs)
                                                gene_var = '{}基因{}第{}位密码子{}置换为{}使得第{}位氨基酸由{}变成了{},此变异在样本中的频率为{}'.format(
                                                    AA2.split(':')[0],
                                                    AA2.split(':')[2],
                                                    AA2.split(':')[3].split('.')[-1][1:-1],
                                                    AA2.split(':')[3].split('.')[-1][0],
                                                    AA2.split(':')[3].split('.')[-1][-1],
                                                    AA2.split(':')[-1].split('.')[-1][1:-1],
                                                    aa_cn[AA2.split(':')[-1].split('.')[-1][0]],
                                                    aa_cn[AA2.split(':')[-1].split('.')[-1][-1]],
                                                    str(freq)[0:6])
                                                line_list.append(gene_var)
                                                s = '\t'.join(line_list)
                                                # print(s)
                                                fw.write(s + '\n')

                                            else:
                                                line_list.append(AA2)
                                                line_list.append('请报告审核者根据hgvs命名提供')
                                                s = '\t'.join(line_list)
                                                #print(s)
                                                fw.write(s + '\n')

                                else:
                                    fw.write(line)


if __name__=='__main__':
    data = '/Users/wjb/Desktop/somatic/NGS180903-11NJ.anno.somatic.hg19_multianno.txt'
    gene_info = '/Users/wjb/Desktop/result/NGS报告改版-知识库-基因介绍.xlsx'
    NM = '/Users/wjb/Desktop/result/NM.xlsx'
    drugs = '/Users/wjb/Desktop/result/靶向用药自动关联.xlsx'
    middleFile = '/Users/wjb/Desktop/somatic/somatic.txt'
    r_w_file = R_W_file(data,gene_info,NM,drugs,middleFile)
    r_w_file.write()