#用于更新交易日信息
from API_TradeDays import TDays
from dateutil.parser import parse
import datetime 
import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
#连接数据库
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/tushare_stockdata?charset=utf8')  

tdays=TDays()
print('获取数据库里面最新的交易日信息')
the_last_day=tdays.GetTradeDays('2018-01-01')[-1][0]
print('获取当前tushare 所具有的最新交易日信息')
re=ts.trade_cal()
re.index=re['calendarDate']
re=re[-500:]
#判断是否需要更新
tradedays=[]
tushare_newest_day=parse(re.iloc[-1]['calendarDate'])
if the_last_day < tushare_newest_day:
    print("需要更新交易日信息")
    flag = False
    for index in re.index:
        parse_days = parse(index)
        if flag or parse_days > the_last_day:
            flag = True
            if re.loc[index]['isOpen'] == 1:
                tradedays.append(parse_days)
    df = pd.DataFrame(tradedays,columns=['date'])
    try:
        pd.io.sql.to_sql(df,'tdays', yconnect, 
                     schema='tdays',index=False,if_exists='append')
        print("数据更新成功")
    except:
        print("无法写入")
else:
    print("数据不需要更新")