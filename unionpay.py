#coding:utf-8
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.preprocessing import scale
from sklearn.svm import SVC
import os

global U,base_w,wmax,M
U=0.01
base_w=0.5
M=25
param_number = 2
# wmax  = 1

base_dir = r'C:\Users\user\Desktop\unionpay\Index_data_201509\Index_data_201509'
target_dir=r'C:\Users\user\Desktop\unionpay\Index_data_201509\Index_data_201509\result'
# new_dir=r'D:\unionpay\PYdata\20151008\MAROC_method'

factor_file = os.path.join(base_dir,'week_adj.csv')
volume_file = os.path.join(base_dir,'week_volume.csv')
price_file = os.path.join(base_dir,'week_price.csv')
cols=['SuperMar','HA_Retailer','Car','Airline','Beverage','Travel','Realest','Retailer']
cols2=['CarSer','Jellery','Catering','ChainHot','LuxHot']
# col_lack=[]

sector_rt = pd.read_csv(price_file,index_col = 0,parse_dates = True)
factor = pd.read_csv(factor_file,index_col = 0,parse_dates = True)
sector_volume = pd.read_csv(volume_file,index_col = 0,parse_dates = True)

sector_rt = sector_rt.iloc[1:]
sector_volume = sector_volume.iloc[1:]
sector_re_avg = sector_rt.mean(axis=1)

factor_rt = factor.copy()
factor_rt.drop(factor_rt.index[0],axis = 0,inplace = True)
factor_rt.iloc[:] = ( factor.iloc[1:].values - factor.iloc[:-1].values )/ factor.iloc[:-1].values

sector_rt.drop(cols2,axis = 1,inplace = True)

factor.drop(cols2,axis = 1,inplace = True)
factor_rt.drop(cols2,axis = 1,inplace = True)
sector_volume.drop(cols2,axis = 1,inplace = True)
sector_volume.apply(scale)

NUM=len(factor.columns)
print NUM

def unionpay_factor(window_length):
    
    day_length = len(sector_rt)
    entrys = pd.DataFrame(0,index = sector_rt.index,columns = sector_rt.columns)
#     pvalues = params.copy()

    for sector in sector_rt.columns:
#         print sector
        secrt = sector_rt[sector]
        secvol = sector_volume[sector]
        secfactor_rt = factor_rt[sector]
        secentry = entrys[sector]
        
        for day in xrange(window_length+1,day_length-1):
            start_day = day - window_length
            end_day   = day
            
            Y = secrt.iloc[start_day:end_day].values
            X1 = secfactor_rt.iloc[start_day-1:end_day-1].values
#             X2 = secvol.iloc[start_day - 1:end_day - 1].values
            X2 = secrt.iloc[start_day - 1:end_day - 1].values
#             X  = np.column_stack((X1,X2,X3))
#             X = np.column_stack((X,Ybefore))
#             X = np.column_stack((X,HS3001.iloc[start_day - 1:end_day - 1].values))

            model = SVC()
#             model.fit(sm.add_constant(X1),Y)
            model.fit(np.column_stack((X1,X2)),Y)
#             forcast = model.predict((secfactor_rt.iloc[end_day],secvol.iloc[end_day],secrt.iloc[end_day]))
            forcast = model.predict((secfactor_rt.iloc[end_day],secrt.iloc[end_day]))
#             forcast = model.predict((1,secfactor_rt.iloc[end_day]))
#             forcast = model.predict(secfactor_rt.iloc[end_day])
                        
            XX = sm.add_constant(secfactor_rt.iloc[start_day -1:end_day -1].values)
            model2 = sm.OLS(Y,XX)
            re = model2.fit()
            forcast2 = re.predict((1,secfactor_rt.iloc[end_day]))
            print "%.4f %.4f %.4f" %(forcast[-1],forcast2[-1],secrt.iloc[end_day+1])
#             secentry.iloc[day] = forcast > U
            secentry.iloc[day] = forcast[-1] > U
#     entrys = entrys.astype(np.bool)
#     entrys = entrys.apply(lambda x:x>0)
    entrys = entrys.astype(np.int)
    return entrys
            

def weight(signal):
    global weights
#     weights = pd.DataFrame(0,index = signal.index,columns = signal.columns)
#     positive_count = signal[ (signal == 1) ].count(axis=1)
    weights=(1-base_w)/(signal.sum(axis=1))*signal+np.float(base_w)/NUM
#     weights=np.minimum((1-base_w)/(signal.sum(axis=1))*signal+np.float(base_w/8),wmax)
#     weights=weights.fillna((1-weights.sum(axis=1))/(8-positive_count))
    weights.fillna(1.0/NUM,inplace = True)
#     print weights
#     weights = weights.apply(scale,axis = 1)
    weights.to_csv(os.path.join(target_dir,'weight'  + '.csv'))
#     print 'ok'
    
    return weights
#   
 
def backtest(ret,stk_data_avg):

    aaa=np.array(ret)+1
    bbb=np.cumprod(aaa)
    bbb=pd.Series(bbb,index=ret.index)
    cum_origin=(stk_data_avg+1).cumprod()
#     print cum_origin
    result=pd.DataFrame(index=stk_data_avg.index,columns=[u'等权行业组合表现',u'策略累计收益率',u'单次收益率'])
    result[u'等权行业组合表现']=cum_origin
    result[u'单次收益率']=ret
    result[u'策略累计收益率']=bbb
    result.to_csv(os.path.join(target_dir,'backtest.csv'),encoding='cp936')

    return result

                 
if __name__ == '__main__':

        entrys = unionpay_factor(M)
        weights = weight(entrys)
        ret=pd.DataFrame(index=sector_rt.index,columns=['ret1'])
        ret=(sector_rt*weights).sum(axis=1)[M:]
        ret.ix[0]=0
        stk_data_avg=sector_rt.mean(axis=1)[M:]
        stk_data_avg.ix[0]=0
        ret_a=backtest(ret,stk_data_avg)   
        print ret_a
        a= np.count_nonzero(ret_a[u'单次收益率']>sector_re_avg[M:])
#         df = pd.DataFrame(np.array([ret_a[u'单次收益率'].values,sector_re_avg[M:].values]))
#         print df.head() 
        b= len(ret_a[u'单次收益率'].values)
        prob=float(a)/float(b)
#         ret_a.to_csv(os.path.join(target_dir,'ret_a.csv'),encoding='cp936')
        
        print a,b
        print "%.4f" % prob 


        
    
    
    