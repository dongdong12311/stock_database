import tushare as ts
import datetime
import pandas as pd
from sqlalchemy import create_engine
from  API_StockCode import CodeManagement
codes=CodeManagement().GetCodeName()
from API_tusharedata import tushareDataDB
database=tushareDataDB()
import pymysql
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/tushare_stockdata?charset=utf8')  
db=pymysql.connect("localhost","root","123123","tushare_stockdata",charset='utf8')
cursor=db.cursor()   
today=datetime.datetime.today()
if today.hour<=18:
    today=today-datetime.timedelta(1)
for code in codes:
    code=code[0]
    sql="""SELECT * FROM tushare_stockdata.`"""+code+"""`
    order by date  desc limit 1"""
    re=()
    try:
        re=database.fetchone(sql)
    except:
        print(code+"is not exist")
        sql = """CREATE TABLE   `tushare_stockdata`.`"""+code+"""` (
          `date` DATE NOT NULL,
          `open` DOUBLE NULL,
          `high` DOUBLE NULL,
          `low` DOUBLE NULL,
          `close` DOUBLE NULL,
          `volume` DOUBLE NULL,
          `price_change`   DOUBLE NULL,
          `p_change` DOUBLE NULL,
          `ma5` DOUBLE NULL,
          `ma10` DOUBLE NULL,
          `ma20` DOUBLE NULL,
          `v_ma5` DOUBLE NULL,
          `v_ma10` DOUBLE NULL,
          `v_ma20` DOUBLE NULL,
          `turnover` DOUBLE NULL,
          PRIMARY KEY (`date`));"""
        cursor.execute(sql)
        db.commit()
    if re is not None and len(re)!=0 :
        lastdate=datetime.datetime(re[0].year,re[0].month,re[0].day)
        begindate=lastdate+datetime.timedelta(1)
        if today<begindate:
            continue
        data=ts.get_hist_data(code,datetime.datetime.strftime(begindate,"%Y-%m-%d"),datetime.datetime.strftime(today,"%Y-%m-%d"))
    else:
        data=ts.get_hist_data(code)
    if data is not None and len(data)>0:
        print("写入"+code)
        pd.io.sql.to_sql(data,code, yconnect, 
                         schema='tushare_stockdata',if_exists='append')