import os
import glob
import pandas as pd


def get_groupvs(path):
    for groupvs in os.listdir(path + '/data'):
        yield groupvs


def generate_file(path, groupvs):
    os.system(f'mkdir {path}/data/{groupvs}/krona')
    os.system(f'mkdir {path}/data/{groupvs}/taxa_tree')
    otu_table = pd.read_csv(f'{path}/data/{groupvs}/01.OTU_Taxa/original/otu_taxa_table.xls', index_col=0, sep='\t')
    with open(f'{path}/data/{groupvs}/sample_info.txt', 'w') as fw:
        samples = otu_table.columns.tolist()
        # print(title.split('\t'))
        fw.write('SampleID\tBarcodeSequence\tLinkerPrimerSequence\tGroup\tDescription\n')
        fg = open(f'{path}/data/{groupvs}/taxa_tree/group.txt', 'w')
        for i in samples[:-1]:
            group = i.split('_')[0]
            fw.write(f'{i}\tATCG\tATCG\t{group}\t{i}\n')
            fg.write(f'{i}\t{group}\n')
            tmp_list = []
            tmp_list.append(i)
            tmp_list.append('taxonomy')
            data = otu_table[tmp_list]
            tax_df = data['taxonomy'].str.split(';', expand=True)
            data = data.drop('taxonomy', axis=1)
            data = pd.concat([data, tax_df], axis=1)
            # print(data.head())
            data.to_csv(f'{path}/data/{groupvs}/krona/{i}.txt', index=False, header=False, sep='\t')

        fg.close()


def krona(path, groupvs):
    os.system(f'mkdir -p {path}/report/{groupvs}/krona')
    file_list = [file for file in glob.glob(f'{path}/data/{groupvs}/krona/*.txt')]
    krona_file = ' '.join(file_list)
    # print(krona_file)
    os.system(f'ktImportText {krona_file} -o {path}/report/{groupvs}/krona/krona.html')

def tree(path, groupvs):
    # os.system(f'mkdir -p {path}/report/{groupvs}/taxa_tree/sample_tree')
    # os.system(f"sed -i 's/d_/k_/g;s/;/; /g' {path}/data/{groupvs}/01.OTU_Taxa/original/otu_taxa_table.xls")
    os.system(f'/usr/bin/python3 /home/apt/Desktop/level_tree/level_tree_sample.py \
                -f {path}/data/{groupvs}/01.OTU_Taxa/original/otu_taxa_table.xls \
                -t 10 -o {path}/report/{groupvs}/taxa_tree/sample_tree')

    os.system(f'/usr/bin/python3 /home/apt/Desktop/level_tree/level_tree.py \
                -f {path}/data/{groupvs}/01.OTU_Taxa/original/otu_taxa_table.xls \
                -t 10 \
                -g {path}/data/{groupvs}/taxa_tree/group.txt \
                -o {path}/report/{groupvs}/taxa_tree')

def anosim(path, groupvs):
    inpath = f'{path}/data/{groupvs}'
    outpath = f'{path}/report/{groupvs}'
    os.system(f'Rscript /home/apt/Desktop/P20190200280-SX1/anosim.R {inpath} {outpath}')

def alpha(path, groupvs):
    # os.system(f'mkdir {path}/report/{groupvs}/Alpha')
    # os.system(f'alpha_diversity.py \
    #             -i {path}/data/{groupvs}/01.OTU_Taxa/normalize/otu_taxa_table.biom \
    #             -o {path}/report/{groupvs}/Alpha/alpha_diversity_index.txt \
    #             -t {path}/otus.tre \
    #             -m shannon,simpson,ace,goods_coverage,chao1,observed_species,PD_whole_tree')
    inpath = f'{path}/data/{groupvs}'
    outpath = f'{path}/report/{groupvs}'
    os.system(f'Rscript /home/apt/Desktop/P20190200280-SX1/AlphaDiversity.R {inpath} {outpath}')

def main():
    path = '/home/apt/Desktop/P20190200280-SX1'
    for i in get_groupvs(path):
        # print(i)
        # generate_file(path, i)
        # krona(path, i)
        # tree(path, i)
        # anosim(path, i)
        if i in ['group1']:
            alpha(path, i)

if __name__ == '__main__':
    main()
