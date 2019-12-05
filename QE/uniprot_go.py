import os
import re
import time
import socket
from tqdm import tqdm
from queue import Queue
from functools import wraps
from threading import Thread
from openpyxl import Workbook
from urllib.request import urlopen
import xml.etree.ElementTree as ET
# from multiprocessing import Pool

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print(f"Total time running: {str(int(t1-t0))} seconds")
        return result
    return function_timer


class Spider():
    def __init__(self, path):
        self.path = path
        self.proid = Queue()
        self.data = list()
        self.thread_num = 20

    def produce_xml(self, dir):
        url = 'http://www.uniprot.org/uniprot/{}.xml'
        file = os.path.join(dir, 'diff_list.txt')
        diff_list = open(file)
        for j in diff_list:
            xml = url.format(j.strip())
            self.proid.put(xml)
        diff_list.close()

    def get_info(self):
        while not self.proid.empty():
            xml = self.proid.get()
            proid = re.split('[/.]', xml)[-2]
            try:
                response = urlopen(xml)
                tree = ET.parse(response)
                root = tree.getroot()
                goid = [child.attrib.get('id') for child in root.iter(tag='{http://uniprot.org/uniprot}dbReference') if child.attrib.get('type') == 'GO']
                tmp = [child.attrib.get('value') for child in root.iter(tag='{http://uniprot.org/uniprot}property') if child.attrib.get('type') == 'term']
                category = [i.split(':')[0] for i in tmp]
                goterm = [i.split(':')[1] for i in tmp]
                proname = ''.join([child.text for child in root.iter(tag='{http://uniprot.org/uniprot}fullName')][0])
                geneid = ''.join([child.attrib.get('id') for child in root.iter(tag='{http://uniprot.org/uniprot}dbReference') if child.attrib.get('type') == 'GeneID'])
                genename = ''.join([child.text for child in root.iter(tag='{http://uniprot.org/uniprot}name') if child.attrib.get('type') == 'primary'])

                # proname = None if len(proname) == 0 else proname
                # geneid = None if len(geneid) == 0 else geneid
                # genename = None if len(genename) == 0 else genename

                bp = set([f'{goterm[k]} [{goid[k]}]' if v == 'P' else '-' for k, v in enumerate(category)])
                mf = set([f'{goterm[k]} [{goid[k]}]' if v == 'F' else '-' for k, v in enumerate(category)])
                cc = set([f'{goterm[k]} [{goid[k]}]' if v == 'C' else '-' for k, v in enumerate(category)])
                all_go = []
                all_go.extend(bp)
                all_go.extend(mf)
                all_go.extend(cc)

                if len(goid) == 0:
                    out = f'{proid}\t{proname}\t{geneid}\t{genename}\t-\t-\t-\t-'.split('\t')
                else:
                    bp = ';'.join(bp)
                    mf = ';'.join(mf)
                    cc = ';'.join(cc)
                    all_go = ';'.join(all_go)
                    out = f'{proid}\t{proname}\t{geneid}\t{genename}\t{bp}\t{mf}\t{cc}\t{all_go}'.split('\t')
                self.data.append(out)

                response.close()
            except Exception as e:
                out = f'{proid}\t-\t-\t-\t-\t-\t-\t-'.split('\t')
                self.data.append(out)
                print(e)
    # print(get_info('A1YZ34'))
    @fn_timer
    def main(self):
        socket.setdefaulttimeout(20)
        wb = Workbook()
        i = 0
        for d in tqdm(os.listdir(self.path)):
            dir = os.path.join(self.path, d)
            if os.path.isdir(dir):
                self.produce_xml(dir)
                threads = []
                for _ in range(self.thread_num):
                    t = Thread(target=self.get_info)
                    time.sleep(1)
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                ws = wb.create_sheet(d, i)
                i += 1
                ws.append(['ProteinID', 'ProteinName', 'GeneID', 'GeneName', 'BP', 'MF', 'CC', 'GO_Term'])
                for j in self.data:
                    # print(j)
                    ws.append(j)
                self.data.clear()

        wb.save(os.path.join(self.path, 'GO.xlsx'))

# if __name__=='__main__':
#     path = 'E:\\GUI\\QE_exe\\Data\\R20190901243'
#     # start = time.time()
#     Spider(path).main()
#     # end = time.time()
#     # print(end - start)
