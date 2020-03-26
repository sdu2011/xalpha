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
    print('份额:{},昨日净值{},当前余额{},总投入{},收益率{}'.format(fe,dqjz,dqye,buy,syl))
    return (fe,dqjz,dqye,buy,syl)

# f(trade_info,code)

read=xa.record("E:\\git\\xalpha\\tests\\fund_2020.csv")
# read.status

jjcode_list = list(read.status.columns.values)[1:] #持有的全部基金列表
t_buy,t_get = 0,0 #总计买入,总计剩余(包括当前剩余及赎回)
for code in jjcode_list:
    trade_info = read.status.loc[:,['date',code]]
    # print(trade_info)

    fe,dqjz,dqye,buy,syl = f(trade_info,code)
    t_buy += buy
    t_get = dqye
print('整体收益率:{}'.format(t_get/t_buy-1))

#添加交易记录 
import pandas as pd
def add_op(date,code,money,csv):
    trade_info=xa.record("E:\\git\\xalpha\\tests\\fund_2020.csv").status
    jjcode_list = list(trade_info.columns.values)[1:] #持有的全部基金列表
    print(trade_info.index.values[-1])
    
    if code in jjcode_list:
        d={'date':date,code:money}
#         print(d)
        new=pd.DataFrame(d,index=[1])   
        trade_info=trade_info.append(new)
        print(trade_info)
    else:
        pass

add_op('2020-03026','163411',4000,"E:\\git\\xalpha\\tests\\fund_2020.csv")







