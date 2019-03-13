import sys
import pandas as pd

site = sys.argv[1]
df = pd.read_csv(site, sep='\t')

new_df = df['Sequence window'].dropna()

with open('motif.txt', 'w') as f:
    for seq in new_df:
        if ';' in seq:
            for s in seq.split(';'):
                f.write(s[int(len(s) / 2) - 6:int(len(s) / 2) + 7] + '\n')
        else:
            # print(len(seq[int(len(seq) / 2) - 6:int(len(seq) / 2) + 6]))
            f.write(seq[int(len(seq) / 2) - 6:int(len(seq) / 2) + 7] + '\n')