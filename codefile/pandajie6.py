f_A=open(r'C:\Users\wjb\Desktop\6\A')
f_B=open(r'C:\Users\wjb\Desktop\6\B')
onlyA=open(r'C:\Users\wjb\Desktop\6\onlyA','w')
onlyB=open(r'C:\Users\wjb\Desktop\6\onlyB','w')
bothAB=open(r'C:\Users\wjb\Desktop\6\bothAB','w')
for i in f_A:
    if i in f_B:
        print(i)
        bothAB.write(i)
