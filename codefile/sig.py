import sys
import os
import pandas as pd
from StyleFrame import StyleFrame, Styler

data_file = os.path.join(sys.argv[1], '质谱鉴定和定量结果', '附件3_蛋白质定量和差异分析列表.xlsx')
out_file = os.path.join(sys.argv[1], '质谱鉴定和定量结果', '附件3_蛋白质定量和差异分析列表2.xlsx')
data = pd.read_excel(data_file, None)

# writer = pd.ExcelWriter('E:\\Project\\Protein\\iTraq_TMT\\P20190600885\\质谱鉴定和定量结果\\text.xlsx')
ew = StyleFrame.ExcelWriter(out_file)

for k in data.keys():
    df = data[k]
    columns = df.columns.tolist()
    # print(df.shape)
    ## 上调
    df_up = df[(df[columns[-1]] < 0.05) & (df[columns[-2]] > 1.2)]
    ## 下调
    df_down = df[(df[columns[-1]] < 0.05) & (df[columns[-2]] < 1/1.2)]
    # print(df_down.shape)
    ## other
    ex_list = list(df_up[columns[0]])
    ex_list.extend(df_down[columns[0]])
    df_ex = df[~df[columns[0]].isin(ex_list)]
    # print(df_ex.shape)
    ## 合并数据
    newdf = pd.concat([df_up, df_down, df_ex], ignore_index=True)
    # print(newdf.index)
    row_num = list(range(1, len(newdf.index) + 2))
    sf = StyleFrame(newdf)
    sf.set_row_height(rows=row_num, height=15)    # 所有行设置行高
    ## 上下调添加颜色
    sf.apply_style_by_indexes(indexes_to_style=sf[(sf[columns[-2]] > 1.2) & (sf[columns[-1]] < 0.05)],
                              styler_obj=Styler(bg_color='red'), cols_to_style=columns[-2])
    sf.apply_style_by_indexes(indexes_to_style=sf[(sf[columns[-2]] < 1/1.2) & (sf[columns[-1]] < 0.05)],
                              styler_obj=Styler(bg_color='green'), cols_to_style=columns[-2])
    sf.to_excel(ew, sheet_name=k)
    # newdf.to_excel(writer, sheet_name=k, index=False)

# writer.save()
# writer.close()

ew.save()

