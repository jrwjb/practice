import os
import re
import glob
import csv
import time
import argparse
import multiprocessing

class QC(object):
    def __init__(self,data_dir):
        self.data_dir = data_dir
        self.rawData = '/Users/wjb/data/RawData'
        self.cleanData = '/Users/wjb/data/CleanData'
        self.unpairedData = '/Users/wjb/data/UnpairedData'
        self.bedPath = '/Users/wjb/data/BedFiles'

    def mkdir(self):
        os.system('mkdir {}/{}'.format(self.cleanData,self.data_dir))
        os.system('mkdir {}/{}'.format(self.unpairedData,self.data_dir))

    def bed(self):
        bed_list = [i for i in glob.glob(self.bedPath + '/*.bed')]
        return bed_list

    def cmd(self):
        file_list,cmds = [],[]
        for file in glob.glob(self.rawData + '/' + self.data_dir + '/*.gz'):
            sample = os.path.basename(file)
            if not sample.startswith('Un'):
                file_list.append('_'.join(sample.split('_')[:-2]))

        for i in set(file_list):
            cmd = 'trimmomatic PE -phred33 {}/{}/{}_R1_001.fastq.gz {}/{}/{}_R2_001.fastq.gz {}/{}/{}_R1.fastq.gz {}/{}/trim.{}_R1_001.fastq.gz /{}/{}/{}_R2.fastq.gz {}/{}/trim.{}_R2_001.fastq.gz ILLUMINACLIP:/Users/wjb/Downloads/trimmomatic-0.38/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:20 LEADING:3 TRAILING:3 MINLEN:35'.format(
                self.rawData , self.data_dir , i , self.rawData , self.data_dir, i , self.cleanData, self.data_dir, i.split('_')[0] , self.unpairedData , self.data_dir, i , self.cleanData , self.data_dir, i.split('_')[0], self.unpairedData , self.data_dir , i)
            cmds.append(cmd)
        return cmds

    def run_cmd(self,cmd):
        os.system(cmd)

    def multiProcess(self):
        pool = multiprocessing.Pool(2)
        for cmd in self.cmd():
            pool.apply_async(self.run_cmd,(cmd,))
        pool.close()
        pool.join()

    def splitDataToPanel(self):
        samplesheet = '{}/{}/SampleSheet.csv'.format(self.rawData,self.data_dir)
        os.system('cp {} {}/{}'.format(samplesheet,self.cleanData,self.data_dir))
        data_path = '{}/{}'.format(self.cleanData,self.data_dir)
        with open(samplesheet) as f:
            filereader = csv.reader(f)
            for i in filereader:
                for j in glob.glob(data_path + '/*.gz'):
                    sample_name = os.path.basename(j).split('_')[0]
                    if sample_name == i[1]:
                        panel = i[6]+self.data_dir.split('_')[0]
                        mk_panel = 'mkdir {}/{}'.format(data_path,panel)
                        os.system(mk_panel)
                        os.system('mv {} {}/{}'.format(j,data_path,panel))
                        os.system('zip -j {}/{}/{}.zip {}/{}/{}*'.format(data_path,panel,sample_name,data_path,panel,sample_name))
                        os.system('rm {}/{}/*.gz'.format(data_path,panel))
                        bedFile = [ bed for bed in self.bed() if re.match(i[6],bed.split('/')[-1])]
                        os.system('cp {} {}/{}'.format(bedFile[0],data_path,panel))

    def main(self):
        self.mkdir()
        self.multiProcess()
        self.splitDataToPanel()

if __name__=='__main__':
    start = time.time()
    parser = argparse.ArgumentParser(description = 'Pre_treatment')
    parser.add_argument('-i','--input',help = 'Input data_dir',required = True)
    parser.add_argument('-e','--example',help = 'python Pre_treatment.py -i /Users/wjb/data/RawData/180921HZ08_NB501078_0004_AHCC5LAFXY')
    args = parser.parse_args()

    data_dir = args.input.split('/')[-1]
    #print(data_dir)
    #data_dir = '180921HZ05_NB501078_0004_AHCC5LAFXY'
    qc = QC(data_dir)
    qc.main()
    end = time.time()
    print('Total time:{}'.format(end - start))





