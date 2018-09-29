import re
import xlrd
from openpyxl import Workbook

class Chemical(object):
    def __init__(self,data,refence,middleFile):
        self._data = data
        self._refence = refence
        self._middleFile = middleFile

    def refence(self):
        refence_table = xlrd.open_workbook(self._refence).sheet_by_index(0)
        refence_dict = {}
        gene_dic = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

        for row in range(refence_table.nrows):
            refence_line = refence_table.row_values(row)
            if row > 0 and refence_line[3].startswith('r'):
                if refence_line[10] == '-':
                    s = refence_line[4].split('/')
                    ss = [gene_dic[i] for i in s]
                    sss = '/'.join(ss)
                    refence_str = refence_line[3] + '-' + sss
                    refence_dict[refence_str] = refence_line[:8]

                else:
                    refence_str = refence_line[3] + '-' + refence_line[4]
                    refence_dict[refence_str] = refence_line[:8]

        return refence_dict

    def writeFile(self):
        data_table = xlrd.open_workbook(self._data).sheet_by_name('SNP')
        title = ['medicineName','geneName','rsId','geneType','medicineType','clinicalGuide','evidenceLevel']

        wb = Workbook()
        ws = wb.active
        ws.append(data_table.row_values(0) + title)

        for row in range(data_table.nrows):
            data_line = data_table.row_values(row)
            if data_line[10].startswith('r'):
                data_str = data_line[10] + '-' + data_line[9]
                if data_str in self.refence():
                    ws.append(data_table.row_values(row) + self.refence()[data_str][1:])

                else:
                    ws.append(data_table.row_values(row))

        wb.save(self._middleFile)


class ResultApi(object):
    def __init__(self,data,api):
        self._data = data
        self._api = api

    def api(self):
        api_table = xlrd.open_workbook(self._api).sheet_by_index(0)
        data_table = xlrd.open_workbook(self._data).sheet_by_index(0)

        wb = Workbook()
        ws = wb.active

        ws.append(api_table.row_values(0))
        ws.append(api_table.row_values(1))

        for row in range(1,data_table.nrows):
            line = data_table.row_values(row)
            medicine = line[22]
            if medicine:
                sample_barcode = line[2][:-2] + ','
                newLine = []
                if re.search(r'/',medicine):
                    medicine_list = medicine.split('/')
                    for i in medicine_list:
                        temp = []
                        temp.extend(sample_barcode.split(','))
                        temp.append(i)
                        temp.extend(line[23:])
                        ws.append(temp)
                else:
                    newLine.extend(sample_barcode.split(','))
                    newLine.extend(line[22:])
                    ws.append(newLine)

        wb.save('/Users/wjb/Desktop/result/chemicalApiTest.xlsx')

if __name__=='__main__':
    data = '/Users/wjb/Desktop/result/data.xls'
    refence = '/Users/wjb/Desktop/result/refence.xlsx'
    middleFile = '/Users/wjb/Desktop/result/chemical.xlsx'
    chemical = Chemical(data,refence,middleFile)
    chemical.writeFile()
    api = '/Users/wjb/Desktop/result/化疗API.xlsx'
    resultApi = ResultApi(middleFile,api)
    resultApi.api()







