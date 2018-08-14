import pymysql

# Connect to the database
# db = pymysql.connect(host='ip',
#                              user='user',
#                              password='password',
#                              db='wjb_data')
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor=db.cursor()
#
# #查看是否有数据表
# #sql='show tables;'
# #cursor.execute(sql)
# #data=cursor.fetchone()
# #print(data)
#
# #创建数据表
# cursor.execute('drop table if exists my_table')
#
# sql='''CREATE TABLE my_table (
#         CHROM text,
#         POS int,
#         ID int,
#         REF text,
#         ALT text,
#         QUAL text,
#         FILTER text,
#         INFO text)'''
# cursor.execute(sql)

#查看数据表内容
#cursor.execute('select * from my_table;')
#data=cursor.fetchone()
#print(data)

# cursor.execute('set @@global.local_infile=1;')

#文件导入数据库
# sql="load data local infile \
#     '/Users/wjb/Desktop/clinvar_20180729.vcf' \
#     into table my_table \
#     fields terminated by 't' \        #  分隔符
#     enclosed by '''' \                # 数据中有引号作为正常字段
#     lines terminated by '\n'          # 换行符
#      ignore 27 lines;"                # 忽略前27行
# cursor.execute(sql)

#插入数据
with open('/Users/wjb/clinvar_20180729.vcf') as f:

    for row in f:
        if not row.startswith('#'):
            print(row)
            row=row.split('\t')
            sql='''insert into my_table(CHROM,POS,ID,REF,ALT,INFO) values('{}',{},{},'{}','{}','{}')'''.format(row[0],row[1],row[2],row[3],row[4],row[7].strip())
            #print(sql)
            cursor.execute(sql)

#cursor.execute("insert into my_table values('7',94037171,432608,'G','C','.','.','ALLELEID=425769;CLNDISDB=MedGen:CN169374;CLNDN=not_specified;CLNHGVS=NC_000007.13:g.94037171G>C;CLNREVSTAT=criteria_provided,_single_submitter;CLNSIG=Uncertain_significance;CLNVC=single_nucleotide_variant;CLNVCSO=SO:0001483;GENEINFO=COL1A2:1278;MC=SO:0001583|missense_variant;ORIGIN=1')")
#
# cursor.execute('select * from my_table;')
# data=cursor.fetchall()
# for i in data:
#     print(i)
#
# cursor.close()
# db.close()