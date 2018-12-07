import os
import re
import argparse


class Sub_fasta(object):
    def __init__(self, path):
        self.path = path

    def mk_dir(self, path):
        os.system('mkdir {}'.format(path + '/' + path.split('/')[-1]))

    def get_file(self, path):
        pattern = re.compile(r'.*_vs_.*')
        groupvs = []
        s_fasta = ''
        for file in os.listdir(path):
            if pattern.search(file):
                groupvs.append(file)
            elif re.search(r'.*.fasta', file):
                s_fasta = re.search(r'.*.fasta', file).group()

        return s_fasta, groupvs

    def sub_fasta(self, path):
        with open(path + '/all_list.txt') as a_list:
            with open(path + '/' + self.get_file(path)[0]) as fasta:
                with open(path + '/all.fasta', 'w') as a_fasta:
                    flag = 0
                    id_list = [i.strip() for i in a_list]
                    for line in fasta:
                        # print(line)
                        if line.startswith('>'):
                            name = line.split('|')[1]
                            if name in id_list:
                                flag = 1
                                # print(line)
                                a_fasta.write('>' + name + '\n')
                            else:
                                flag = 0
                        else:
                            if flag == 0:
                                pass
                            else:
                                a_fasta.write(line)

    def cp_file(self, path):
        os.system('cp {} {}'.format(path + '/all_list.txt', path + '/' + path.split('/')[-1]))
        os.system('cp {} {}'.format(path + '/all.fasta', path + '/' + path.split('/')[-1]))
        for file in self.get_file(path)[1]:
            os.system('cp -r {} {}'.format(path + '/' + file, path + '/' + path.split('/')[-1]))

    def main(self):
        self.mk_dir(path)
        self.get_file(path)
        self.sub_fasta(path)
        self.cp_file(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract fasta')
    parser.add_argument('-i', '--input', help='input the path of project', required=True)
    args = parser.parse_args()
    path = args.input
    sub_fa = Sub_fasta(path)
    sub_fa.main()