import xalpha as xa
from datetime import date

def get_info(code): #传入code,取得在该基金上的投资信息
    read=xa.record('../tests/fund_2020.csv')
    jj_list = list(read.status.columns.values)[1:] #持有的全部基金列表
    print(jj_list)

    
    xqjx = xa.fundinfo(code) #兴全精选
    print(xqjx.info())
    xqjx_trade = xa.trade(xqjx,read.status) 
    report = xqjx_trade.dailyreport() #截止昨日的信息总结,包含持有份额,当日净值,单位成本等信息.
    print(type(report))
    earning = report.at[0,'基金收益总额']
    print(earning)

get_info('163411')







curr_day = date.today().strftime('%y-%m-%d')
