#读取数据
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
import os
year = 2021
list=[]
list.append('year')
list.append('Gini')
list_year=[]
list_Gini=[]
figure_save_path="GINIfiles"
if not os.path.exists(figure_save_path):
    os.makedirs(figure_save_path)
for i in range(1):
    del list[0]
    del list[0]
    df1=pd.read_csv(r'C:\Users\wuhui\Desktop\HoneyCreek_NitrateCQ(2).csv')
    df1=df1.dropna().reset_index(drop=True)
    #df1.info()
    df1['Date']=pd.to_datetime(df1['Date'])
    df=df1[df1['Date'].apply(lambda x: x.year ==year)]
    df.to_csv(r'C:\Users\wuhui\Desktop\export1.csv',index=True,header=True)
    df2=pd.read_csv(r'C:\Users\wuhui\Desktop\export1.csv')
    df2['Flow_cum']=df2['Flow'].cumsum()
    df2['Flow_ratio']=df2['Flow']/df2['Flow'].sum()*100
    df2['Solute_cum']=df2['Solute'].cumsum()
    df2['Solute_ratio']=df2['Solute']/df2['Solute'].sum()*100
    df2['S/F']=df2['Solute_ratio']/df2['Flow_ratio']
    df2.to_csv(r'C:\Users\wuhui\Desktop\export2.csv',index=True,header=True)
    df3=pd.read_csv(r'C:\Users\wuhui\Desktop\export2.csv')
    df3.sort_values(by='S/F',inplace=True,ascending=True)
    df3.to_csv(r'C:\Users\wuhui\Desktop\export3.csv',index=True,header=True)
    #print(df3)
    df4=pd.read_csv(r'C:\Users\wuhui\Desktop\export3.csv')
    df4['time_ratio_cum']=df4['Flow_ratio'].cumsum()
    df4['Lorenz curve']=df4['Solute_ratio'].cumsum()
    df4['avg']=df4['time_ratio_cum']
    df4.to_csv(r'C:\Users\wuhui\Desktop\export4.csv', index=True, header=True)
    df4.plot(x='time_ratio_cum',y=['Lorenz curve','avg'])
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.savefig(os.path.join(figure_save_path,str(year)))
    plt.show()
    plt.close()
#面积A+B=100*100*0.5=5000
#面积B
    s=0
    for i in df4.index[1:]:
        Flow1=df4.loc[i-1,'Lorenz curve']
        Flow2=df4.loc[i,'Lorenz curve']
        Flow_ratio=df4.loc[i,'Flow_ratio']
        s+=(Flow1+Flow2)*Flow_ratio*0.5
    Gini=round((100*100*0.5-s)/(100*100*0.5),3)
    list.append(year)
    list.append(Gini)
    print(list)
    print
    list_year.append(year)
    list_Gini.append(Gini)
    year = year + 1
plt.plot(list_year, list_Gini,'g-s')
plt.ylabel('基尼系数')
plt.xlabel('年')
plt.ylim(0,1)
plt.xlim(2017,2022)
plt.xticks(range(2017,2022,1))
plt.show()
