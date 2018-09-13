import xlrd
import csv


data = xlrd.open_workbook('/Users/wjb/Desktop/data/data.xls')
refence = xlrd.open_workbook('/Users/wjb/Desktop/data/refence.xlsx')

write_file = open('/Users/wjb/Desktop/data/test2.xls','w',encoding='utf-8-sig')

file_writer = csv.writer(write_file,dialect='excel')

data_table = data.sheet_by_name('SNP')
refence_table = refence.sheets()[0]

#对参考数据创建字典索引
gene_dic = {'A':'T','T':'A','C':'G','G':'C'}
refence_dict = {}
for row in range(refence_table.nrows):
    refence_line = refence_table.row_values(row)
    if row >0 and refence_line[3].startswith('r'):
        if refence_line[10] =='-':
            s = refence_line[4].split('/')
            ss = [gene_dic[i] for i in s]
            sss = '/'.join(ss)
            #refence_str = refence_line[3] + '-' + refence_line[4]
            refence_str = refence_line[3] + '-' + sss
            refence_dict[refence_str] = refence_line[:7]

        else:
            refence_str = refence_line[3] + '-' + refence_line[4]
            refence_dict[refence_str] = refence_line[:7]


# for row in range(refence_table.nrows):
#     refence_line = refence_table.row_values(row)
#     if row > 0 and refence_line[3].startswith('r'):
#         if refence_line[10] =='-':
#             s = refence_line[4].split('/')
#             ss = [gene_dic[i] for i in s]
#             sss = '/'.join(ss)
#             print(refence_line[4])
#             print(sss)
#             print('########')


ll = ['medicineName','geneName','rsId','geneType','medicineType','clinicalGuide']
#写入第一行
file_writer.writerow(data_table.row_values(0)+ll)
#写入匹配参考的行及其他行
for row in range(data_table.nrows):
    data_line = data_table.row_values(row)
    if data_line[10].startswith('r'):
        data_str = data_line[10] + '-' + data_line[9]
        if data_str in refence_dict.keys():
            file_writer.writerow(data_table.row_values(row)+refence_dict[data_str][1:])
            #pass

        else:
            file_writer.writerow(data_table.row_values(row))
            #pass


write_file.close()

