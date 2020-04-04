#coding=utf-8
import sys
sys.path.insert(0, "../../")

import xalpha as xa
print(xa.__path__)
from datetime import date

from datetime import date
from datetime import datetime, timedelta
today = date.today()
today = today.strftime("%Y-%m-%d")

def get_jz(code,date):
    fundinfo = xa.fundinfo(code)
    df=fundinfo.price
    dwjz = df[df['date']==date]['netvalue'] #获取某一日期净值
    
    for index in dwjz.index:
        # print('{},date:{}单位净值为:{}'.format(fundinfo.name,date,dwjz.get(index)))
        return dwjz.get(index)
    
def f(trade_info,code): #某个基金的交易信息
    fundinfo = xa.fundinfo(code)

    buy,sell=0,0
    fe=0
    for index, row in trade_info.iterrows():
        date = row.get('date')
        dwjz = get_jz(code,date)

        v = row.get(code)
        if v > 0:
            buy += v
        else:
            sell += v

        fe += v/dwjz #份额变动
    
    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    dqjz = get_jz(code,yesterday) #api接口到24点以后才更新净值,所以做多只能取到昨日净值
    dqye = fe*dqjz+sell #包括当前持有金额以及已卖出金额之和
    syl = dqye/buy-1#收益率
    print('{},{}--份额:{},昨日净值{},当前余额{},总投入{},收益率{},盈利{}'.format(fundinfo.name,yesterday,fe,dqjz,dqye,buy,syl,dqye-buy))
    return (fe,dqjz,dqye,buy,syl)

# f(trade_info,code)

read=xa.record("../tests/fund_2020.csv")
# read.status

jjcode_list = list(read.status.columns.values)[1:] #持有的全部基金列表
t_buy,t_get = 0,0 #总计买入,总计剩余(包括当前剩余及赎回)
for code in jjcode_list:
    trade_info = read.status.loc[:,['date',code]]
    # print(trade_info)

    fe,dqjz,dqye,buy,syl = f(trade_info,code)
    t_buy += buy
    t_get += dqye
print('总投入:{},总回报:{},整体收益率:{},盈利{}'.format(t_buy,t_get,t_get/t_buy-1,t_get-t_buy))

#添加交易记录 
import pandas as pd
def add_op(date,code,money,csv):
    trade_info=xa.record(csv).status
    jjcode_list = list(trade_info.columns.values)[1:] #持有的全部基金列表
    # print(trade_info.index.values[-1])
    
    #把每行的时间格式改掉
    for index, row in trade_info.iterrows():
        date = row.get('date') #2020-02-21 00:00:00 timestamp
        # print(type(date)
        trade_info.at[index,'date'] = date.strftime("%Y%m%d")
    print(trade_info)

    if code in jjcode_list:
        d={'date':date,code:money}
        new=pd.DataFrame(d,index=[1])
        trade_info=trade_info.append(new,ignore_index=True,sort=False)
        trade_info.fillna(0,inplace=True) #注意inplace=True才能更改掉trade_info
        print(trade_info)

        #把float->int 比如1000.00改为1000
        for column in trade_info.columns:
            # print(column)
            if column != 'date':
                trade_info[column] = trade_info[column].astype(int)
                # print(trade_info[column])

        trade_info.to_csv('../tests/new_fund_2020.csv',index=False)
    else:
        pass
# test
# add_op('20200326','163411',4000,"../tests/fund_2020.csv")

# 计算沪深300收益率
def get_300():
    beginday='20200221'
    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    begin = get_jz('510300',beginday)
    end = get_jz('510300',yesterday)
    print('同期510300收益率:{}'.format((end/begin - 1.0)))

get_300()