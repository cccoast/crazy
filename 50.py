#coding:utf-8
'''
@attention: PCF FOR 000049/510070
@author: ChuQ
@version: 0.1
@license: Open Source, Any one can use it on any purpose
@contact: xdi@pbc.gov.cn
@time: 20140901
'''
import StringIO
import pandas as pd
import numpy as np
import os
import time
import datetime
import xlrd
import dbf
    
''' MAKE SURE '''   
today = 20140829
yestday = 20140828
tomorrow = 20140901
index_name = '000049'
fund_name  = '510070'
base_dir = r'C:\Users\user\Desktop\deal\deal\deal\20140829\input'
position_ratio = 0.995

''' NO NEED TO CHANGE '''
etfTmrName = r'%s%04d.etf' %(fund_name,tomorrow%10000)
etfTodayName = r'%s%04d.etf' %(fund_name,today%10000)
netValue = r'ETFFUNDPCF%d.dbf' %(tomorrow)
weightYest = r'%sweightnextday%d.xls' %(index_name,yestday) 
weightToday = r'%sweightnextday%d.xls' %(index_name,today) 

etfTodayPath = os.path.join(base_dir,etfTodayName)
etfTmrPath= os.path.join(base_dir,etfTmrName)
netValuePath = os.path.join(base_dir, netValue)
weightYestPath = os.path.join(base_dir,weightYest)
weightTodayPath = os.path.join(base_dir,weightToday)
target_path = os.path.join(base_dir,'test.xls')
wind_path   =  os.path.join(base_dir,'wind.xls')

float_zero = 0.00000001
def almost_same(a,b):
    return np.abs(a - b) < 0.00001
     
def dbf_parser(dbf_path):
    
    tmpfile = os.path.join(base_dir,'$dbf.csv')
#     print dbf_path,tmpfile
    dbf_reader(dbf_path,tmpfile)
    return pd.read_csv(tmpfile)
    
def dbf_reader(dbf_path,csv_path):
    table = dbf.Table(dbf_path,codepage = 'cp936')
    table.open()
    dbf.export(table,csv_path,encoding = 'utf-8')

def xls_reader(xls_path,csv_path):
    table = pd.read_excel(xls_path)
    table.to_csv(csv_path,index = False)

def pcf_parser(etf_path):
    
    fund_summary = []
    fund_detail = []
    exception_tag = ['[ETFMQ]','TAGTAG','ENDENDEND']
    stage = 0

    with open(etf_path,'r') as etf_today_in:
        for line in etf_today_in:
            _line = line.strip()
#             print _line
#             print _line.decode('cp936')
            if _line not in exception_tag:
                if stage == 1:
                    fund_summary.append(_line.strip())#(_line.decode('cp936'))
                elif stage == 2:
                    fund_detail.append(_line.strip())#(_line.decode('cp936'))
            else:   
                if _line == exception_tag[0]:
                    stage += 1
                elif _line == exception_tag[1]:
                    stage += 1
                elif _line == exception_tag[2]:
                    stage += 1
    if stage != 3:
        print '--->>> Format Wrong!!'

#     print fund_summary
#     print fund_detail
    summary_df = pd.read_csv(StringIO.StringIO(os.linesep.join(fund_summary)),sep = '=',header = None,\
                             names = ['field','value'],encoding = 'cp936')
    detail_df  = pd.read_csv(StringIO.StringIO(os.linesep.join(fund_detail)),sep = '|',\
                            names = ['field','value','quant','flag','ratio','cash','extra'],\
                             header = None,encoding = 'cp936')
#     print summary_df.head()
#     print detail_df.head()
    fields = pd.DataFrame(columns = ['field','value','quant','flag','ratio','cash','extra'])
    fields.loc[0] = ['[ETFMQ]',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    total_df = pd.concat((fields,summary_df))
    
    fields = pd.DataFrame(columns = ['field','value','quant','flag','ratio','cash','extra'])
    fields.loc[0] = ['TAGTAG',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    total_df = pd.concat((total_df,fields))
    
    tag1 = pd.Series(index = ['field','value','quant','flag','ratio','cash','extra'])
    total_df = pd.concat((total_df,detail_df))
    
    fields = pd.DataFrame(columns = ['field','value','quant','flag','ratio','cash','extra'])
    fields.loc[0] = ['ENDENDEND',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    total_df = pd.concat((total_df,fields))
    
    total_df = total_df[['field','value','quant','flag','ratio','cash','extra']]
    
    summary_df.index = summary_df['field']
    detail_df.index = detail_df['field']
    total_df.index = total_df['field']
    
    detail_df['cash'] =  detail_df['cash'].apply(lambda x:x.decode('cp936').strip()).apply(lambda x: np.float(x) if x != u'' else np.nan)
    detail_df['ratio'] =  detail_df['ratio'].apply(lambda x:x.decode('cp936').strip()).apply(lambda x: np.float(x) if x != u'' else np.nan) 
    detail_df[u'value'] =  map(lambda x:x.decode('utf-8').strip(),detail_df[u'value'].values)  
     
    return total_df,summary_df,detail_df
       
class DataCheck(object):
    
    def __init__(self,df_today,df_yest,excel_out,final_row,final_col):
        
        date1,date2 = df_today[u'生效日期'].iloc[0],df_yest[u'生效日期'].iloc[0]
        if date1 <= date2:
            print 'Date Error!'
        print 'today = ',date1,'yestday = ',date2
        wind_df = pd.read_excel(wind_path,index = u'code')
        date = wind_df[u'date'].iloc[0]
        self.wind_prices = wind_df[u'price']
        
        outcols = map(lambda x:x.strip(),u'指数代码     股票代码    股票名称    收盘价    权重变化<10%'.split())
        self.outdf = pd.DataFrame(columns = outcols,index = df_today[u'成分券代码'])
        self.outdf[u'指数代码'] = [ index_name ] * len(self.outdf)
        self.df_today,self.df_yest = df_today,df_yest
        
        self.final_row = final_row
        self.final_col = final_col
        
    def code_cmp(self):
        self.outdf[u'股票代码'] = np.equal( self.df_today[u'成分券代码'] , self.df_yest[u'成分券代码'] )
        
    def name_cmp(self):
        self.outdf[u'股票名称'] = np.equal( self.df_today[u'成分券名称'], self.df_yest[u'成分券名称'] )
    
    def price_cmp(self):
        self.df_today[u'收盘'].astype(float)
        self.outdf[u'收盘价'] = ( np.abs( self.wind_prices - self.df_today[u'收盘'].values ) < 0.001 ).values
        
    def weight_cmp(self):
        name = self.df_today.columns[-4]
        self.outdf[self.outdf.columns[-1]] = ( np.abs( ( self.df_today[name] - self.df_yest[name] ) / self.df_yest[name] ) < 0.1001 )
        
    def run(self):
        self.code_cmp()
        self.name_cmp()
        self.price_cmp()
        self.weight_cmp()
        self.outdf.to_excel(excel_out, u'数据来源',encoding = 'utf-8')
        
        new_df = self.outdf.describe()
        new_df.loc[u'正常值'] = self.outdf.apply(np.count_nonzero)
        new_df.to_excel(excel_out, u'数据来源',encoding = 'utf-8',startrow = 0,startcol = len(self.outdf.columns) + 5)
        new_df.to_excel(excel_out, u'最终表',encoding = 'utf-8',startrow = self.final_row,startcol = self.final_col)
        
        self.final_row += len(new_df.index) + 2
#         self.final_col += len(new_df.columns) + 2
        
        print 'Data Check Finished!'
        return self.final_row,self.final_col

class PCFCheck(object):
    
    def __init__(self,today_wt,yest_wt,pcf_detail_tmr,pcf_detail_today,pcf_summary_tmr,pcf_summary_today,netDf,excel_out,final_row,final_col):
        
        cols = map(lambda x:x.strip(),u'股票代码    股票名称    数量    数量2    数量3   现金替代标志      比例'.split())
        self.outdf = pd.DataFrame(columns = cols,index = pcf_detail_tmr['field'])
        self.today_wt = today_wt
        self.yest_wt  = yest_wt
        self.pcf_detail_tmr = pcf_detail_tmr
        self.pcf_detail_today  = pcf_detail_today 
        self.pcf_summary_tmr = pcf_summary_tmr
        self.netDf = netDf
        self.final_row = final_row
        self.final_col = final_col
        
    def run(self):
        self.outdf[u'股票代码'] =( self.today_wt[u'成分券代码'] == self.pcf_detail_tmr[u'field'] )
        self.outdf[u'股票名称'] =( self.today_wt[u'成分券名称'] == self.pcf_detail_tmr[u'value'] )
#         print self.outdf[u'股票名称']
        redem_unit = ( self.pcf_summary_tmr.loc[ (self.pcf_summary_tmr['field'] == 'CreationRedemptionUnit') ]['value'] ).values
        net_value = ( self.netDf[str.lower('JJZJZ')]/self.netDf[str.lower('JJZFE')] ).values

        self.outdf[u'数量'] =  redem_unit * position_ratio * net_value * self.today_wt[u'权重(%)'] / ( 100 * self.today_wt[u'调整后开盘参考价'] )
        self.outdf[u'数量2'] = map(np.int,( np.round( np.round(self.outdf[u'数量'] + float_zero) / 100 ) * 100 ))
        self.outdf[u'数量3'] = np.equal(self.outdf[u'数量2'],self.pcf_detail_tmr['quant'])
        self.outdf[u'现金替代标志'] = (self.pcf_detail_tmr['flag'] == 1).values

        self.outdf[u'比例'] = (almost_same(self.pcf_detail_tmr['ratio'].values , float(0.1)))
        self.outdf.to_excel(excel_out, u'PCF检查',encoding = 'utf-8')
        
        new_df = self.outdf.describe()
        new_df.loc[u'正常值'] = self.outdf.apply(np.count_nonzero)
        new_df.to_excel(excel_out, u'PCF检查',encoding = 'utf-8',startrow = 0,startcol = len(self.outdf.columns) + 5)
        new_df.to_excel(excel_out, u'最终表',encoding = 'utf-8',startrow = self.final_row,startcol = self.final_col)
        self.final_row += len(new_df.index) + 2
        
#         self.final_col += len(new_df.columns) + 2
        print 'PCF Check Finished!'
        return self.final_row,self.final_col

class SummaryCheck(object):
    
    def __init__(self,today_wt,yest_wt,pcf_detail_tmr,pcf_detail_today,pcf_summary_tmr,pcf_summary_today,netDf,excel_out,final_row,final_col):
        
        self.final_row = final_row
        self.final_col = final_col
        
        self.outdf = pd.DataFrame(columns = map(lambda x:x.strip(),u'预估现金部分 预估现金部分比较 交易日 现金差额 现金差额比较 最小申购赎回单位资产净值比较 基金份额净值'.split()),\
                             index  = range(1))
        
        nav_per_unit = pcf_summary_tmr.loc[ pcf_summary_tmr['field'] == 'NAVperCU']['value'].values[0]

        cash_swap = pcf_detail_tmr['cash'].sum()
        valid_index =  pcf_detail_tmr['flag'].astype(np.int) <= 1 
        market_value = ( pcf_detail_tmr.loc[valid_index]['quant'] * today_wt.loc[valid_index][u'调整后开盘参考价'] ).sum()
        estimate_cash = nav_per_unit - cash_swap - market_value
        EstimateCashComponent = pcf_summary_tmr.loc[ pcf_summary_tmr['field'] == 'EstimateCashComponent' ]['value'][0]
        
        _cash_swap = pcf_detail_today['cash'].sum()
        _valid_index =  pcf_detail_today['flag'].astype(np.int) <= 1 
        _market_value = ( pcf_detail_today.loc[_valid_index]['quant'] * today_wt.loc[_valid_index][u'收盘'] ).sum()
        _cash = nav_per_unit - _cash_swap - _market_value
        CashComponent = pcf_summary_tmr.loc[pcf_summary_tmr['field'] == 'CashComponent' ]['value'][0]
        
        dbf_nav_per_unit = netDf['jzdwjjjz'].iloc[0]
        
        dbf_NAV = netDf['dwjjjz'].iloc[0]
        NAV     = pcf_summary_tmr.loc[ pcf_summary_tmr['field'] == 'NAV' ]['value'][0]
        
        trading_day = pcf_summary_tmr.loc[ pcf_summary_tmr['field'] == 'TradingDay' ]['value'][0]
        
        self.outdf.loc[0][map(lambda x:x.strip(),u'预估现金部分 预估现金部分比较 交易日 现金差额 现金差额比较 最小申购赎回单位资产净值比较 基金份额净值'.split())] = \
                    [estimate_cash,almost_same(estimate_cash,EstimateCashComponent),tomorrow == trading_day,\
                     _cash,almost_same(_cash,CashComponent),almost_same(dbf_nav_per_unit,nav_per_unit),\
                     almost_same(dbf_NAV,NAV)]
                    
        self.excel_out = excel_out
        print 'Summary Check Finished'
        print [estimate_cash,almost_same(estimate_cash,EstimateCashComponent),tomorrow == trading_day,\
                     _cash,almost_same(_cash,CashComponent),almost_same(dbf_nav_per_unit,nav_per_unit),\
                     almost_same(dbf_NAV,NAV)]
        
    def run(self):
        self.outdf.to_excel(self.excel_out, u'最终表',  index = False, encoding = 'utf-8',startrow = self.final_row,startcol = self.final_col)
        
if __name__ == "__main__":
    
    final_row = 0
    final_col = 0

    netDf = dbf_parser(netValuePath)
#     print netDf.columns

    yestDf = pd.read_excel(weightYestPath,encoding = 'cp936',parse_dates = u'生效日期',index = '指数代码\n\Index Code')
    yestDf.columns = map(lambda x:x.split('\n')[0],yestDf.columns)
    yestDf[u'成分券名称'] = yestDf[u'成分券名称'].apply(lambda x:x.strip())
    yestDf.index = yestDf[u'成分券代码']

    todayDf = pd.read_excel(weightTodayPath,encoding = 'cp936',parse_dates = u'生效日期')
    todayDf.columns = map(lambda x:x.split('\n')[0],todayDf.columns)
    todayDf[u'成分券名称'] = todayDf[u'成分券名称'].apply(lambda x:x.strip())
    todayDf.index = todayDf[u'成分券代码']

    pcf_today,pcf_summary_today,pcf_detail_today = pcf_parser(etfTodayPath)
    pcf_tmr,pcf_summary_tmr,pcf_detail_tmr = pcf_parser(etfTmrPath)
    
    with pd.ExcelWriter(target_path) as excel_out:
        
        netDf.to_excel(excel_out,sheet_name = u'净值表',encoding = 'utf-8',index = False)
        yestDf.to_excel(excel_out,sheet_name = u'昨日权重表',encoding = 'utf-8',index = False)
        todayDf.to_excel(excel_out,sheet_name = u'今日权重表',encoding = 'utf-8',index = False) 
        pcf_today.to_excel(excel_out,sheet_name = u'PCF%d' %(today),encoding = 'utf-8',index = False,header = None)
        pcf_tmr.to_excel(excel_out,sheet_name = u'PCF%d' %(tomorrow),encoding = 'utf-8',index = False,header = None)
        
        data_check = DataCheck(todayDf,yestDf,excel_out,final_row,final_col)
        final_row,final_col = data_check.run()
        
        pcf_check = PCFCheck(todayDf,yestDf,pcf_detail_tmr,pcf_detail_today,pcf_summary_tmr,pcf_summary_tmr,netDf,excel_out,final_row,final_col)
        final_row,final_col = pcf_check.run()
        
        summary_check = SummaryCheck(todayDf,yestDf,pcf_detail_tmr,pcf_detail_today,pcf_summary_tmr,pcf_summary_tmr,netDf,excel_out,final_row,final_col)
        summary_check.run()
        
        
        
        
        
        