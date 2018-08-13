import re
import time
import pandas as pd
import numpy as np

t1=time.time()

file='/Users/wjb/Desktop/CCDS.current 2.txt'
df=pd.read_table(file)

def df_fun(df):
    df_1=df.replace('-',-1)
    df_2=df_1.replace('+',-1)
    df_3=df_2.fillna(-1)
    df_4=df_3.astype(int)
    df_5=df_4+1
    df=df_5.replace(0,np.nan)
    return df

df.cds_from=df_fun(df.cds_from)
df.cds_to=df_fun(df.cds_to)


df_location=df.cds_locations.dropna(how='all')
df_location_1=df_location.replace('-','[0]')

list1=[]
for row in df_location_1:
    row=row.strip('[]')
    temp = re.split(r'[,-]', row)
    for i,j in enumerate(temp):
        temp[i]=str(int(j)+1)
    list2 = []
    str1 = ''
    addition_number = 0
    i = 1
    while addition_number < len(temp):
        while i <= 2:
            if addition_number > len(temp) - 1:
                break
            else:
                str1 = str1 + temp[addition_number]+'-'
                addition_number += 1
            i += 1
        list2.append(str1.strip('-'))
        str1 = ''
        i = 1
    list1.append(list2)
df_list=pd.Series(list1)
df.cds_locations=df_list

#去重复
df_cds_locations=df.cds_locations.dropna(how='all')
df_gene=df.gene.dropna(how='all')


ll=[]
for i in range(len(df_gene)):
    temp = df.cds_locations[i]
    j=i+1
    while j< len(df_gene) and df_gene[j]==df_gene[i]:
        temp.extend(df.cds_locations[j])
        temp=sorted(set(temp))
        df.cds_locations[j]=temp
        j+=1

    ll.append(str(temp))

# ll=[]
# for i in range(len(df_gene)):
#     temp = df.cds_locations[i]
#     for j in range(1,len(df_gene)):
#         if df_gene[j]==df_gene[i]:
#             temp.extend(df.cds_locations[j])
#             temp=sorted(set(temp))
#     #print(temp)
#     ll.append(str(temp))

df_ll=pd.DataFrame(pd.Series(ll))
df_no_dup=df_ll.drop_duplicates()
df.cds_locations=df_no_dup
#print(df.cds_locations)

df.to_csv('/Users/wjb/Desktop/test.txt',index=False,sep='\t')

t2=time.time()
print(t2-t1)













# df_cds_locations=df.cds_locations.dropna(how='all')
# df_gene=df.gene.dropna(how='all')
#
# # print(len(df_gene),len(df_cds_locations))
#
# for i in df_cds_locations.index:
#     temp1=df_cds_locations[i].strip('[]').split(',')
#     j=i+1
#     if j<len(df_cds_locations):
#         temp2=df_cds_locations.iloc[j].strip('[]').split(',')
#         for k in range(len(temp1)):
#             if temp2[k] in temp1:
#                 del temp2[k]
#
#
#                 print(temp2)



# def no_duplicate():
#     for i in df_cds_locations.index:
#         temp1=df_cds_locations.iloc[i].strip('[]').split(',')
#         temp2=df_cds_locations.iloc[i+1].strip('[]').split(',')
        # for j in range(len(temp1)):
        #     if temp2[j] in temp1:
        #         del temp2[j]
    #return temp2


# no_duplicate()

    #print(temp1)
#df.to_csv('/Users/wjb/Desktop/test.txt',index=False,sep='\t')
# print(len(df_cds_locations))

# l=[]
# with open(file) as f:
#     for row in f:
#         s=row.split('\t')[7]
#         l.append(s)
# print(l)