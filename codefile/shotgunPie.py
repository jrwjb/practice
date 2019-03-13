# import pyecharts
import pandas as pd
from pyecharts import Pie, Grid, configure, Line

configure(output_image=True)

# go = pd.read_csv('/home/apt/Project/Protein/Shotgun/P20181201191/P20181201191_vs_N_proteins/go/GOLevel2.txt', sep='\t')
#
# go_bp = go[go['Type'] == 'biological_process']
# go_cc = go[go['Type'] == 'cellular_component']
# go_mf = go[go['Type'] == 'molecular_function']
#
# # print(go_bp)
# pie_bp = Pie("Biological Process", title_pos='center', width=1080, height=720)
# pie_bp.add("BP", go_bp['Term'], go_bp['Seqs'], label_text_size=10, radius=[0, 50], is_legend_show=False, is_label_show=True)
# # pie_bp.render(path='/home/apt/Desktop/GOLevel2_BP.html')
# pie_bp.render(path='/home/apt/Desktop/GOLevel2_BP.pdf')
#
# # grid = Grid()
# # grid.add(pie_bp)
# # grid.render(path='/home/apt/Desktop/GOLevel2_BP.pdf')
#
#
# pie_cc = Pie('Cellular Component', title_pos='center', width=1080, height=720)
# pie_cc.add('CC', go_cc['Term'], go_cc['Seqs'], label_text_size=10, radius=[0, 50], is_legend_show=False, is_label_show=True)
# # pie_cc.render(path='/home/apt/Desktop/GOLevel2_CC.html')
# pie_cc.render(path='/home/apt/Desktop/GOLevel2_CC.pdf')
#
# #
# #
# pie_mf = Pie('Molecular Function', title_pos='center', width=1080, height=720)
# pie_mf.add('MF', go_mf['Term'], go_mf['Seqs'], label_text_size=10, radius=[0, 50], is_legend_show=False, is_label_show=True)
# # pie_mf.render(path='/home/apt/Desktop/GOLevel2_MF.html')
# pie_mf.render(path='/home/apt/Desktop/GOLevel2_MF.pdf')


#
# def my_pie(data1, data2, my_title):
#     pie = Pie(my_title, title_pos='center', width=900)
#     pie.add(my_title, data1, data2, center=[50, 50], is_label_show=True, is_legend_show=False)
#     pie.render()



kegg = pd.read_csv('/home/apt/Project/Protein/Shotgun/P20181201191/P20181201191_vs_N_乙酰化修饰_K/kegg/map2query.txt', sep='\t')

# kegg = pd.read_csv('E:\\Project\\Protein\\Shotgun\\P20181201191\\P20181201191_vs_N_乙酰化修饰_K\\kegg\\map2query.txt', sep='\t')
kegg_top20 = kegg.sort_values(by=['Seqs_Num'], ascending=False).iloc[0:20]
#
# print(kegg_top20)
#
pie_kegg = Pie('KEGG Pathways(Top 20)', title_pos='center')
pie_kegg.add('kegg', kegg_top20['Map_Name'], kegg_top20['Seqs_Num'], label_text_size=8, radius=[0, 60], is_legend_show=False, is_label_show=True)
# pie_kegg.render(path='C:\\Users\\jbwang\\Desktop\\TopMapStatPie.png')

grid = Grid()
grid.add(pie_kegg)
grid.render(path='/home/apt/Desktop/TopMapStatPie.pdf')
# pie_kegg.print_echarts_options()


# columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
# data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
#
#
# # //设置主标题与副标题，标题设置居中，设置宽度为900
# pie = Pie("饼状图", "一年的降水量与蒸发量",title_pos='center',width=900)
# # //加入数据，设置坐标位置为【25，50】，上方的colums选项取消显示
# # pie.add("降水量", columns, data1,center=[25,50],is_legend_show=False)
# # //加入数据，设置坐标位置为【75，50】，上方的colums选项取消显示，显示label标签
# pie.add("蒸发量", columns, data2,center=[75,50],is_legend_show=False,is_label_show=True)
# # //保存图表
# pie.render(path='C:\\Users\\jbwang\\Desktop\\pie.html')


# line = Line("折线图示例", width=1200)
# attr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
# line.add("最高气温", attr, [11, 11, 15, 13, 12, 13, 10],
#          mark_point=["max", "min"], mark_line=["average"])
# line.add("最低气温", attr, [1, -2, 2, 5, 3, 2, 0], mark_point=["max", "min"],
#          mark_line=["average"], legend_pos="20%")
# attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
# v1 = [11, 12, 13, 10, 10, 10]
# pie = Pie("饼图示例", title_pos="45%")
# pie.add("", attr, v1, radius=[30, 55],
#         legend_pos="65%", legend_orient='vertical')
#
# grid = Grid()
# # grid.add(line, grid_right="65%")
# grid.add(pie, grid_left="60%")
# grid.render(path='C:\\Users\\jbwang\\Desktop\\grid.pdf', delay=3)