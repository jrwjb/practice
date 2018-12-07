import os
from sub_fasta import Sub_fasta
import argparse

class Ex_fasta(object):
    def __init__(self, path):
        self.path = path

    def ex_fasta(self, f_list):
        with open(f_list + '/diff_list.txt') as diff_list:
            with open(path + '/all.fasta') as a_fasta:
                with open(f_list + '/diff.fasta', 'w') as d_fasta:
                    flag = 0
                    id_list = [i.strip() for i in diff_list]
                    # print(id_list)
                    for line in a_fasta:
                        if line.startswith('>'):
                            name = line.strip()[1:]
                            if name in id_list:
                                flag = 1
                                d_fasta.write('>' + name + '\n')
                            else:
                                flag = 0
                        else:
                            if flag == 0:
                                pass
                            else:
                                d_fasta.write(line)

    def main(self):
        file_list = Sub_fasta.get_file(self, path)[1]
        for file in file_list:
            f_list = path + '/' + file
            self.ex_fasta(f_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract fasta')
    parser.add_argument('-i', '--input', help='input the path of project', required=True)
    args = parser.parse_args()
    path = args.input
    ex_fa = Ex_fasta(path)
    ex_fa.main()
