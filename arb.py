
import pandas as pd
import numpy as np
import os
import time
import datetime
import functools

base_dir = r'C:\Users\user\Desktop\arbtrage'
output_file = os.path.join(base_dir,'out.csv')
a_file = os.path.join(base_dir,'aprice.csv')
b_file = os.path.join(base_dir,'bprice.csv')
nv_file = os.path.join(base_dir,'nav.csv')
pre_file = os.path.join(base_dir,'premium.csv')

adf = pd.read_csv(a_file,index_col = 0,parse_dates = True)
bdf = pd.read_csv(b_file,index_col = 0,parse_dates = True)
nvdf = pd.read_csv(nv_file,index_col = 0,parse_dates = True)
predf = pd.read_csv(pre_file,index_col = 0,parse_dates = True)

trading_days = map(lambda x:pd.to_datetime(str(x)),adf.index)
tday2nday = pd.Series(range(len(trading_days)),index = trading_days)
day_range = range(len(trading_days))
nday2tday = pd.Series(map(lambda x:x.year*10000 + x.month *100 + x.day,trading_days),day_range)

#print trading_days

#datadf = pd.read_csv(data_file,encoding = 'cp936',na_values = ['.'],parse_dates = 'n_date',dtype = {'c_parent_code':str})
#datadf.dropna(subset = ['c_parent_code'],axis = 0,inplace = True)
#datadf['c_parent_code'] = datadf['c_parent_code'].apply(lambda x:int(str(x).split('.')[0]))
#print datadf['c_parent_code']
#for col in datadf.columns[3:]:
#    table = pd.pivot_table(datadf,index = 'n_date', columns = 'c_parent_code', values = col)
#    table.to_csv(os.path.join(base_dir,'.'.join((col,'csv'))))

def tday_shift(tday,shift_day = 1):
    if isinstance(tday,str):
        tday = pd.to_datetime(tday)
    elif isinstance(tday,int) or isinstance(tday,np.integer):
        tday = pd.to_datetime(str(tday))
    return trading_days[ tday2nday[tday] + shift_day ]

ftday2nday = lambda x:tday2nday[x]
adf.index = map(ftday2nday,adf.index)
bdf.index = map(ftday2nday,bdf.index)
nvdf.index = map(ftday2nday,nvdf.index)
predf.index = map(ftday2nday,predf.index)

adf.columns = map(lambda x:int(x.split('.')[0]),adf.columns)
bdf.columns = map(lambda x:int(x.split('.')[0]),bdf.columns)
nvdf.columns = map(lambda x:int(x.split('.')[0]),nvdf.columns)
predf.columns = map(lambda x:int(x.split('.')[0]),predf.columns)

print len(adf.index)

start,end = 20120101,20150920
dollar = 10000

NONE = 0
PRE_ARB = 1
DIS_ARB = 2
OPEN = 1
CLOSE = 2

order_df = pd.DataFrame(index = range(100000),columns = ['id','direction','offset','day','rmb','pnl','entry_no','holdday'])
ids = np.array( map(np.int,pd.unique(adf.columns)))
pnl_df = pd.DataFrame(index = day_range,columns = ids)
rmb_df = pd.DataFrame(index = day_range,columns = ['CumRMB'])
print len(ids)

order_no = 0
up_thres = 0.08
low_thres = -0.06
cost_pre = 0.013 
cost_dis = 0.007

def get_price(inddf,day,id):
    day = day if day > 0  else 0
    return inddf.loc[day][id]

def add_order(id,direction,offset,day,rmb,entry_no):
    
    global order_no
    order = order_df.loc[order_no]
    order_no += 1
    order['id'],order['direction'],order['offset'],order['day'] = id,direction,offset,day
    if offset == OPEN:
        order['rmb'] = rmb
        order['entry_no'] = order_no - 1
        return order_no - 1
    elif offset == CLOSE:
        if direction == PRE_ARB:
            netvalue =  get_price(nvdf,day - 3,id)
            aprice   = get_price(adf,day,id)
            bprice   = get_price(bdf,day,id)
            ratio = ( (aprice + bprice) -  netvalue * 2 ) / ( netvalue * 2 )
            irmb = order_df.loc[entry_no]['rmb'] 
            pnl = irmb * ( ratio - cost_pre)
        elif direction == DIS_ARB:
            netvalue =  get_price(nvdf,day,id)
            aprice   = get_price(adf,day -2,id)
            bprice   = get_price(bdf,day -2,id)
            ratio = (  - (aprice + bprice) +  netvalue * 2 ) / ( aprice + bprice)
            irmb = order_df.loc[entry_no]['rmb']
            pnl = irmb * ( ratio - cost_dis)
        order['pnl'],order['entry_no'] = pnl,entry_no
        order['holdday'] = day - order_df.loc[entry_no]['day']
        pnl_df.loc[day][id] = pnl    
        return order_no - 1,irmb,pnl
            
def back_test(start,end):
    
    nav_chgrate = lambda day,id: (get_price(nvdf,day,id) - get_price(nvdf,day - 1,id))/get_price(nvdf,day - 1,id)
    
    global order_no
    start = tday2nday[ tday2nday.index >= pd.to_datetime(str(start)) ].iloc[0]
    end   = tday2nday[ tday2nday.index <= pd.to_datetime(str(end)) ].iloc[-1]
    entry_list = {}
#    print ids
    _ids = np.array( map(np.int,pd.unique(adf.columns)))
    ids = pd.Series(_ids,index = range(len(_ids)))
    entry_list = list()    
    rmb_avalible = dollar
    nextday_rmb_avalible = 0
    
    print start,end
    #conditions
    exit1 = lambda order,day: order['direction'] == PRE_ARB and (order['day'] <= day - 3) 
    exit2 = lambda order,day: order['direction'] == DIS_ARB and (order['day'] <= day - 2)
    entry1 = lambda day,id: ( get_price(predf,day,id) > up_thres or get_price(predf,day,id) < low_thres ) \
                            and (get_price(nvdf,day,id) < 1.47 and get_price(bdf,day,id) > 0.3)   \
                            and abs(nav_chgrate(day,id)) < 0.2
#    entry2 = lambda day,id: (get_price(nvdf,day,id) < 1.47 and get_price(bdf,day,id) > 0.3)       
#    def entry1(day,id,thres):
#        pre = get_price(predf,day,id)
#        return np.abs(pre) > thres

    #back_test

    for day in range(start,end):
        print trading_days[day]
        valid_ids = ids.loc[ np.logical_not( np.isnan(nvdf.loc[day]) ).values  ]
        # test exit
#        if tday2nday[pd.to_datetime('20130711')] == day:
#            print 'fuck u',entry_list
        pops = []
        for entry_ordno in entry_list:    
            order = order_df.loc[entry_ordno]
            if exit1(order,day):
                new_order_no,rmb,pnl = add_order(order['id'],PRE_ARB,CLOSE,day,0.0,entry_ordno)
                pops.append(entry_ordno)
                rmb_avalible += rmb + pnl
            elif exit2(order,day):
                new_order_no,rmb,pnl = add_order(order['id'],DIS_ARB,CLOSE,day,0.0,entry_ordno)
                pops.append(entry_ordno)
                nextday_rmb_avalible += rmb + pnl             
            else:
                pass
        if len(pops) >= 1:
            for i in pops:
                entry_list.remove(i)
        #test entry     
        print 'RMB = ',rmb_avalible
        rmb_df.loc[day]['CumRMB'] = rmb_avalible           
        entry_number = 0
        para_entry1 = functools.partial(entry1,day)
        entryids = filter(para_entry1,valid_ids)
#        para_entry2 = functools.partial(entry2,day)
#        entryids2 = filter(para_entry2,valid_ids)
#        entryids = set.intersection(entryids,entryids2)
        entry_number = len(entryids)
#        print get_price(predf,day,163109)
#        print rmb_avalible
        if entry_number > 0 and rmb_avalible > 1.0 and day < end - 4 :
            irmb = rmb_avalible / entry_number
            print irmb,entryids
            for id in entryids:
                if get_price(predf,day,id) > 0:
                    iorder_no = add_order(id,PRE_ARB,OPEN,day,irmb,0)
                elif get_price(predf,day,id) < 0:
                    iorder_no = add_order(id,DIS_ARB,OPEN,day,irmb,0)
                entry_list.append(iorder_no)
            rmb_avalible = 0.0
            
        rmb_avalible += nextday_rmb_avalible
        nextday_rmb_avalible = 0
    
    outdf = order_df.loc[:order_no-1]
    outdf['day'] = outdf['day'].apply(lambda x:nday2tday[x])
    pnl_df.index = map(lambda x:nday2tday[x],pnl_df.index)
    rmb_df.index = map(lambda x:nday2tday[x],rmb_df.index)
    order_file = os.path.join(base_dir,'order.csv')
    pnl_file   = os.path.join(base_dir,'pnl.csv')
    outdf.to_csv(order_file)
    pnl_df.to_csv(pnl_file)
    
    pnl_df.apply(np.sum,axis = 0).to_csv(os.path.join(base_dir,'every_fund_pnl.csv'))
    pnl_df.apply(np.sum,axis = 1).to_csv(os.path.join(base_dir,'every_day_pnl.csv'))
    rmb_df.to_csv(os.path.join(base_dir,'rmb_every_day.csv'))
   
if __name__ == '__main__':
    back_test(start,end)
