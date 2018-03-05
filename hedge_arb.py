''' copyright by xudi personal '''
''' all rights reserved!!'''

import pandas as pd
import numpy as np
import os
import time
import datetime
import functools
import matplotlib.pyplot as plt

base_dir = r'C:\Users\user\Desktop\arbtrage\hedge'

a_file = os.path.join(base_dir,'aprice.csv')
b_file = os.path.join(base_dir,'bprice.csv')
nv_file = os.path.join(base_dir,'nav.csv')
pre_file = os.path.join(base_dir,'premium.csv')
index_file = os.path.join(base_dir,'index_price.csv')
weight_file = os.path.join(base_dir,'weight.csv')

date2num = lambda x:x.year*10000 + x.month *100 + x.day
code2num = lambda x:int(x.split('.')[0]) 
aprice_df = pd.read_csv(a_file,index_col = 0,parse_dates = True)
codes = map(code2num,aprice_df.columns)
tdays = aprice_df.index
ndays = range(len(tdays))
nday2tday = pd.Series(data = tdays,index = ndays)
tday2nday = pd.Series(data = ndays,index = tdays)

adf = pd.read_csv(a_file,index_col = 0,parse_dates = True)
bdf = pd.read_csv(b_file,index_col = 0,parse_dates = True)
nvdf = pd.read_csv(nv_file,index_col = 0,parse_dates = True)
predf = pd.read_csv(pre_file,index_col = 0,parse_dates = True)
indexdf = pd.read_csv(index_file,index_col = 0,parse_dates = True)
indexdf.columns = map(lambda x:(x.split('.')[0]) ,indexdf.columns)
indexdf = indexdf.loc[indexdf.index >= adf.index[0]]

adf.index,adf.columns = tday2nday[adf.index],codes
bdf.index,bdf.columns = tday2nday[bdf.index],codes
nvdf.index,nvdf.columns = tday2nday[nvdf.index],codes
predf.index,predf.columns = tday2nday[predf.index],codes
indexdf.index = tday2nday[predf.index]

underly = '000016'
start,end = 20150601,20151001

order_no = 0
up_thres = 0.03
low_thres = -0.01
cost_pre = 0.002 
cost_dis = 0.006
up_clear_p,down_clear_b,max_chg_rate_p = 1.40,0.45,0.2

NONE = 0
PRE_ARB = 1
DIS_ARB = 2
OPEN = 1
CLOSE = 2

PRE_ARB_CLEAR = 3
DIS_ARB_CLEAR = 2

UNIT = 1000000
BETA = 1
POSITION_ADJUST = 200

portfolio_df = pd.read_csv(weight_file,index_col = 0)
portfolio_ids = portfolio_df.index.values

order_df = pd.DataFrame(index = range(100000),\
                        columns = ['id','direction','offset','day','nav',
                                   'pnl','entry_no','holdday','entry_spread'])
portfolio_amount_df = pd.DataFrame(0.0,index = ndays,columns = portfolio_ids)
portfolio_quant = pd.DataFrame(0.0,index = ndays ,columns = portfolio_ids)
index_amount = pd.Series(0.0,index = ndays,dtype = np.float)
pnl_df = pd.DataFrame(index = ndays,columns = portfolio_ids)

PRE_ARB_MARK = pd.Series([True]*len(portfolio_ids),portfolio_ids)
DIS_ARB_MARK = pd.Series([True]*len(portfolio_ids),portfolio_ids)

def get_price(inddf,day,id):
    return inddf.loc[day][id]

def add_order(id,direction,offset,day,nav,entry_no):
    
    global order_no
    order = order_df.loc[order_no]
    order_no += 1
    order['id'],order['direction'],order['offset'],order['day'],order['nav'] = id,direction,offset,day,nav
    order['entry_spread'] = get_price(predf,day,id)
    pnl = 0.0
    if offset == OPEN:
        order['entry_no'] = order_no - 1
        if direction == PRE_ARB:
            PRE_ARB_MARK[id] = False
        if direction == DIS_ARB: 
            DIS_ARB_MARK[id] = False
        return order_no - 1
    elif offset == CLOSE:
        entry_order = order_df.loc[entry_no]
        if direction == PRE_ARB:
            netvalue =  get_price(nvdf,day - PRE_ARB_CLEAR + 1,id)
            aprice   = get_price(adf,day - PRE_ARB_CLEAR + 1,id)
            bprice   = get_price(bdf,day - PRE_ARB_CLEAR + 1,id)
            ratio = ( (aprice + bprice) -  netvalue * 2 ) / ( netvalue * 2 ) 
#             print ratio,entry_order['nav']
            pnl = entry_order['nav'] * (ratio - cost_pre)
            PRE_ARB_MARK[id] = True
        elif direction == DIS_ARB:
            netvalue =  get_price(nvdf,day - DIS_ARB_CLEAR,id)
            aprice   = get_price(adf,day - DIS_ARB_CLEAR,id)
            bprice   = get_price(bdf,day - DIS_ARB_CLEAR,id)
            ratio = (  - (aprice + bprice) +  netvalue * 2 ) / ( aprice + bprice)
            pnl = entry_order['nav'] * ( ratio - cost_dis)
#             print ratio,entry_order['nav'] 
            DIS_ARB_MARK[id] = True
        order['pnl'],order['entry_no'] = pnl,entry_no
        order['holdday'] = day - order_df.loc[entry_no]['day']
        pnl_df.loc[day][id] = pnl    
        return order_no - 1,pnl
            
def back_test(start,end):
    
    cycle = 1
    nav_chgrate = lambda day,id: (get_price(nvdf,day,id) - get_price(nvdf,day - 1,id))/get_price(nvdf,day - 1,id)

    global order_no
    global portfolio_df,portfolio_ids,order_df,portfolio_amount_df,portfolio_quant,index_amount,pnl_df
    
    start = tday2nday[ tday2nday.index >= pd.to_datetime(str(start)) ].iloc[0]
    end   = tday2nday[ tday2nday.index <= pd.to_datetime(str(end)) ].iloc[-1]
#     ids = pd.Series(codes,index = range(len(codes)))
    pnls = list()
    pnls2 = list()
    entry_list = list()    
   
    ''' portfolio initialization'''
    ''' T0 NAV = UNIT * (1 + BETA) '''

    portfolio_amount_df.loc[start] = portfolio_df['weight'] * UNIT
    cash = UNIT * ( 1 - portfolio_df['weight'].sum())
    index_amount.loc[start] = UNIT * BETA
    fund_navs = np.array([get_price(nvdf,start,i) for i in portfolio_ids],dtype = np.float)
    portfolio_quant.loc[start] = portfolio_amount_df.loc[start] / fund_navs
    
    '''conditions'''
    exit1 = lambda order,day: order['direction'] == PRE_ARB \
                        and (order['day'] <= day - PRE_ARB_CLEAR) 
    exit2 = lambda order,day: order['direction'] == DIS_ARB \
                        and (order['day'] <= day - DIS_ARB_CLEAR)
    entry1 = lambda day,id: ( get_price(predf,day,id) > up_thres  \
                              or get_price(predf,day,id) < low_thres ) \
                        and (get_price(nvdf,day,id) < up_clear_p  \
                             and get_price(bdf,day,id) > down_clear_b) \
                        and abs(nav_chgrate(day,id)) < max_chg_rate_p 

    for iday,day in enumerate(range(start,end)):
        valid_ids = [ i for i in portfolio_ids if ( get_price(adf,day,i) > 0.0001) ]
        pops = []
        for entry_ordno in entry_list:    
            order = order_df.loc[entry_ordno]
            if exit1(order,day):
                _order_no,pnl = add_order(order['id'],PRE_ARB,CLOSE,day,0.0,entry_ordno)
                pops.append(entry_ordno)
                pnls.append(pnl)
                pnls2.append(pnl)
            elif exit2(order,day):
                _order_no,pnl = add_order(order['id'],DIS_ARB,CLOSE,day,0.0,entry_ordno)
                pops.append(entry_ordno)  
                pnls.append(pnl) 
                pnls2.append(pnl)          
            else:
                pass
        if len(pops) >= 1:
            for i in pops:
                entry_list.remove(i)
        #test entry     
                  
         
        para_entry1 = functools.partial(entry1,day)
        entryids = filter(para_entry1,valid_ids)
        entry_number = len( entryids )

        if entry_number > 0 and day < end - 2 :
            for _id in entryids:
                if get_price(predf,day,_id) > 0.0001 \
                         and (PRE_ARB_MARK[_id] == True) and (DIS_ARB_MARK[_id] == True):
                    iorder_no = add_order(_id,PRE_ARB,OPEN,day,portfolio_amount_df.loc[day][_id],0)
                    entry_list.append(iorder_no)
                elif get_price(predf,day,_id) < -0.0001 and (DIS_ARB_MARK[_id] == True):
                    iorder_no = add_order(_id,DIS_ARB,OPEN,day,portfolio_amount_df.loc[day][_id],0)
                    entry_list.append(iorder_no)
            
        '''clear'''
        price0 = np.array([get_price(nvdf,day,i) for i in portfolio_ids],dtype = np.float)
        price1 = np.array([get_price(nvdf,day+1,i) for i in portfolio_ids],dtype = np.float)
        rate = (price1 - price0)/price0
        rate = np.array(map(lambda x:x[0] if x[1] > 0.001 else 0.0,zip(rate,price0)))
        
        portfolio_amount_df.loc[day + 1] = portfolio_amount_df.loc[day] * (1 + rate) 
        portfolio_quant.loc[day + 1] = portfolio_quant.loc[day]
        index_amount.loc[day+1] = index_amount.loc[day] * \
                (1 + ((get_price(indexdf,day,underly) -\
                get_price(indexdf,day + 1,underly)))/get_price(indexdf,day,underly))       

        if (iday + 1) % POSITION_ADJUST != 0:
            portfolio_amount_df.loc[day + 1] = portfolio_amount_df.loc[day] * (1 + rate) 
            portfolio_quant.loc[day + 1] = portfolio_quant.loc[day]
            index_amount.loc[day+1] = index_amount.loc[day] * (1 + ((get_price(indexdf,day,underly) - get_price(indexdf,day + 1,underly)))/get_price(indexdf,day,underly))       
        else:
            pnl_cum = sum(pnls)
            pnls = []
            cum_NAV = ( index_amount.loc[day] + pnl_cum + cash + portfolio_amount_df.loc[day].sum() ) / (UNIT * (1 + BETA))
            print 'REBALANCE, NAV = ',cum_NAV
            
            ''' Adjust Position Like T0 '''
            portfolio_amount_df.loc[day] = portfolio_df[portfolio_df.columns[cycle%2 ]] * cum_NAV  * UNIT
            cash = ( cum_NAV * UNIT ) * ( 1 - portfolio_df[portfolio_df.columns[cycle%2 ]].sum())
            portfolio_quant.loc[day] = portfolio_amount_df.loc[day] / price0
            index_amount.loc[day] = cum_NAV * BETA * UNIT
            
            portfolio_amount_df.loc[day + 1] = portfolio_amount_df.loc[day] * (1 + rate) 
            portfolio_quant.loc[day + 1] = portfolio_quant.loc[day]
            index_amount.loc[day+1] = index_amount.loc[day] * (1 + ((get_price(indexdf,day,underly) - get_price(indexdf,day + 1,underly)))/get_price(indexdf,day,underly))
        
            cycle += 1
#         print iday,index_amount[iday],(1 + ((get_price(indexdf,day,underly) - get_price(indexdf,day + 1,underly)))/get_price(indexdf,day,underly))
            
        if iday == 0:
            print tdays[day]
        if iday > 0:
            print tdays[day], \
            'Total = ',(index_amount.loc[day]  + cash + np.sum(portfolio_amount_df.loc[day]) + np.sum(pnls))/(UNIT * (1 + BETA)) ,\
            'portfolio = ',np.sum(portfolio_amount_df.loc[day]),\
            ' index = ',index_amount.loc[day],\
            ' cumPNL = ',np.sum(pnls2),\
            ' cash = ',cash
    
    print 'Total signals = ',order_no / 2
    if order_no == 0:
        exit()
    
    trans_df_index = lambda x: map(lambda y:nday2tday[y],x.index)
    outdf = order_df.loc[:order_no-1]
    outdf['day'] = outdf['day'].apply(lambda x:nday2tday[x])
    
    pnl_df,portfolio_amount_df,
    pnl_df.index = trans_df_index(pnl_df)
    portfolio_amount_df.index = trans_df_index(portfolio_amount_df)
    portfolio_quant.index = trans_df_index(portfolio_quant)
    index_amount.index = trans_df_index(index_amount)
    
    order_file = os.path.join(base_dir,'order.csv')
    pnl_file   = os.path.join(base_dir,'pnl.csv')
    position_file = os.path.join(base_dir,'portfolio_position.csv')
    pt_nav_file   = os.path.join(base_dir,'portfolio_nav.csv')
    index_nav_file   = os.path.join(base_dir,'index_amount.csv')
    
    portfolio_amount_df.iloc[start-1:].to_csv(pt_nav_file)
    index_amount.iloc[start-1:].to_csv(index_nav_file)
    portfolio_quant.iloc[start-1:].to_csv(position_file)
    outdf.iloc[start-1:].to_csv(order_file)
    pnl_df.iloc[start-1:].to_csv(pnl_file)
    
    pnl_df.apply(np.sum,axis = 0).to_csv(os.path.join(base_dir,'every_fund_pnl.csv'))
    pnl_df.apply(np.sum,axis = 1).to_csv(os.path.join(base_dir,'every_day_pnl.csv'))
   
if __name__ == '__main__':
    back_test(start,end)
