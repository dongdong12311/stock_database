from API_TradeDays import TDays
from API_StockCode import CodeManagement
from API_IpoDate import IpodateManagement
tdays=TDays()
import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from dateutil.parser import parse
#sql连接
import sys
from API_winddata import WindDataDB
def fetchall(sql):
    cursor.execute(sql)
    db.commit()
    return cursor.fetchall()
def write(datestr,dataslice):
    print("写入"+datestr)
    pd.io.sql.to_sql(dataslice,datestr, yconnect, 
                     schema='stockslice',index=False,if_exists='append')    
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/stockslice?charset=utf8')  
db=pymysql.connect("localhost","root","123123","stockslice",charset='utf8')
cursor=db.cursor()   
ipodates=IpodateManagement()
sql="""show tables"""
re=fetchall(sql)[-1][0]
begindate=datetime.datetime.strftime(parse(re)+datetime.timedelta(1),"%Y-%m-%d")
begindate=tdays.GetTradeDays(begindate)[0][0]
today=datetime.datetime.today()
if today.hour<=18:
    today=today-datetime.timedelta(1)
if today<begindate:
    sys.exit()
print("数据开始更新")
print(begindate)
print(today)
start=datetime.datetime.strftime(begindate,"%Y-%m-%d")
end=datetime.datetime.strftime(today,"%Y-%m-%d")
tradedays=tdays.GetTradeDays(start,end)
stockdata=WindDataDB()
codesM=CodeManagement()
codes=codesM.GetCodeName()
stocks={}
for code in codes:
    code=code[0]
    ipodate=ipodates.GetIpodate(code)[1]
    if ipodate<parse(end):
        print("读取"+code+"数据")
        s=list(stockdata.readDatas(code,start,end))
        if (len(s)>0):
            s=pd.DataFrame(s)
            s.index=s[0]
            s.columns=['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHG', 'PCT_CHG',
                           'ADJFACTOR', 'TURN', 'VOL_RATIO', 'INDUSTRY_CSRC12', 'FREE_TURN',
                           'PE_TTM', 'PB_LF', 'CODE']
            stocks[code]=s
for date in tradedays:
    print(date)
    date=date[0]
    datestr=datetime.datetime.strftime(date,'%Y-%m-%d')
    dataslice=pd.DataFrame(columns=['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHG', 'PCT_CHG',
                           'ADJFACTOR', 'TURN', 'VOL_RATIO', 'INDUSTRY_CSRC12', 'FREE_TURN',
                           'PE_TTM', 'PB_LF', 'CODE'])
    for key in stocks.keys():
        try:
            dataslice=dataslice.append(stocks[key].loc[date])
        except:
            try:
                dataslice=dataslice.append(stocks[key].loc[datetime.date(date.year,date.month,date.day)])
            except:    
                continue
        
    if len(dataslice)>0:
        write(datestr,dataslice)