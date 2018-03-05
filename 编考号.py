# -*- coding: gbk -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import matplotlib as mpt
import os
import re

bsdir = r'E:\2015\exam'
number_pattern = re.compile('\d+')
str_pattern = re.compile(r'[\s\n\t\r]+')

decode_utf8 = lambda x:x.decode('utf-8')
decode_cp936 = lambda x:x.decode('cp936')
encode_utf8 = lambda x:x.encode('utf-8')
encode_cp936 = lambda x:x.encode('cp936')

def nparse(x):
    if isinstance(x,str) or isinstance(x,unicode):
        numbers = number_pattern.findall(x)
        if len(numbers) == 1:
            return '{0:0>2}+{1:0>2}'.format(int(numbers[0]),0)
        else:
            return ''.join(('{0:0>2}+{1:0>2}'.format(int(numbers[0]),int(numbers[1])),x[number_pattern.search(x,2).endpos:]))
    elif isinstance(x,int):
        return '{0:0>2}+{1:0>2}'.format(x,0)
    else:
        return x
    
def exempt_exam(x):
    
    man_birth = 6000
    woman_birth = 6500
    age = int(x[u'出生年月'].split('+')[0]) * 100 + int(x[u'出生年月'].split('+')[1])
    if ( x[u'性别'] == u'男' and age <= man_birth ):
        return 1
    elif ( x[u'性别'] == u'女' and age <= woman_birth ):
        return 2
    elif ( x[u'学历及学位'].find('博士') > -1 ):
        return 3
    else:
        return 0
          
def number():
    fname = r'branch_summary.xls'
    sheet_names = [u'经济',u'会计',u'工程',u'政工']
    col_names = [u'出生年月',u'参加工作时间',u'入行时间',u'本专业工作年限',u'何时何方式取得何技术资格',u'聘任年限']
    infile = os.path.join(bsdir,fname)
    f = lambda x: ''.join(str_pattern.split(x)) if (isinstance(x,unicode) or isinstance(x,str)) else x
    exempt_total = 0
    for snumber,isheet in enumerate(sheet_names):
        df = pd.read_excel(infile,isheet,index_col = 0)
        df.columns = map(f,df.columns)
        df = df.apply(lambda x:x.apply(f))
        df[col_names] = df[col_names].apply(lambda x:x.apply(nparse))
        df['exempt_exam'] = df.apply(exempt_exam,axis = 1)
        iexempt = (df['exempt_exam'] != 0).sum() 
        exempt_total += iexempt
        num_series = np.arange(1500001 + (snumber+1) * 1000,1500001 + (snumber+1) * 1000 +len(df.index) - iexempt )
        df['exam_no'] = None
        np.random.shuffle(num_series)
        df.loc[ ( df['exempt_exam'] == 0 ) ,'exam_no'] = num_series
        df.to_csv(decode_cp936(os.path.join(bsdir,isheet + '.csv')))
        print exempt_total
    return 0

def age():
    base_dir = r'E:\2015\age'
    bins = np.array([50,60,70,80])
    for root,sub,fnames in os.walk(base_dir):
        for ifile in fnames:
            print decode_cp936(ifile)
            infile = os.path.join(root,ifile)
            df = pd.read_csv(infile,encoding = 'cp936')
            df['age'] = df[decode_utf8('出生年月')].apply(lambda x: 10*(int(number_pattern.findall(x)[0])/10))
            ofile = os.path.join(root,ifile.split('.')[0])+'2.csv'
            print decode_cp936(ofile)
            df.to_csv(ofile)
            
def stat():
    base_dir = r'E:\2015\ages'
    out_dir  = r'E:\2015\stats'
    statvs = ['admin','branch','age','level']
    statvs_cn = ['职级','分行','年龄','机构层级']
    xtick = {}
    xtick[1] = np.array(['','上海','天津','沈阳','南京','济南','武汉','广州','成都','西安','北京','重庆'])
    xtick[0] = np.array(['','副科','正科','副处','正处','其他'])
    xtick[2] = np.array(['','80后','70后','60后','50后'])
    xtick[3] = np.array(['','厅局级机构','地市中支','县支行'])
    myfont = mpt.font_manager.FontProperties(fname='C:\Windows\Fonts\msyh.ttf')
    mpl.rcParams['axes.unicode_minus'] = False
    def age_map(x):
        if x == 80:
            return 1
        elif x == 70:
            return 2
        elif x == 60:
            return 3
        elif x == 50:
            return 4
    for root,sub,fnames in os.walk(base_dir):
        for ifile in fnames:
            print ifile
            infile = os.path.join(root,ifile)
            outfile = os.path.join(out_dir,ifile.split('.')[0] + '.png') 
            df = pd.read_excel(infile,encoding = 'cp936')
            df['age'] = df['age'].apply(age_map)
            df.dropna(subset = ['score',],how ='any',inplace = True)
            df.dropna(subset = ['admin',],how ='any',inplace = True)
            df[statvs].astype(np.int)
#             df['level'] = df['level'].apply()
            fig = plt.figure(figsize = (18,12))  
            mean_score = df['score'].mean()
            quantile10 = df['score'].quantile(0.10)
            plt.suptitle('{0}系列考试结果 均分 = {1:.2f}，10%分位数(合格线) = {2}'.format(ifile.split('.')[0],mean_score,quantile10),fontproperties=myfont)
            for ifig,istat in enumerate(statvs): 
                ax1 = fig.add_subplot(2,2,ifig+1)
                odf = []
                means = []
                df = df.sort(istat)
                xtick_index = np.array([int(i) for i in set(df[istat].values)])
                for name,sub_df in df.groupby(istat):
                    print name
                    odf.append(sub_df['score'].values)
                    means.append(sub_df['score'].mean())
                ax1.boxplot(odf,vert = True)
                ax1.set_xticklabels(xtick[ifig][xtick_index],fontproperties=myfont)
                ax1.plot(range(1,len(odf) + 1),means,label = 'mean score')
                ax1.legend(loc = 'best')
                ax1.set_title(statvs_cn[ifig],fontproperties=myfont)
                ax1.grid()
            fig.savefig(outfile,format = 'png')
            plt.show()
            plt.clf()
            plt.close()
            
                       
if __name__ == '__main__':
#     number()
#     age()
    stat()