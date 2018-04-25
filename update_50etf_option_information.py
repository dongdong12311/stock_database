import pymysql    
import pandas as pd
import os,sys
from sqlalchemy import create_engine  
import numpy as np
import datetime
from WindPy import *
from WindPy import w
from dateutil.parser import parse
w.start()
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/50etf_option?charset=utf8')  
db=pymysql.connect("localhost","root","123123","50etf_option",charset='utf8')
cursor=db.cursor()

#获取已有的数据
sql="SELECT wind_code,contract_state FROM 50etf_option.information"
try:
    cursor.execute(sql)
    db.commit()
except:
    sql = """CREATE TABLE  50etf_option.information (
      `wind_code` VARCHAR(10) NOT NULL,
      `sec_name` VARCHAR(20) NULL,
      `call_or_put` VARCHAR(6) NULL,
      `exercise_price` DOUBLE NULL,
      `contract_unit` INT NULL,
      `limit_month` VARCHAR(20) NULL,
      `listed_date` VARCHAR(20) NULL,
      `exercise_date` DATETIME NULL,
      `settlement_date` DATETIME NULL,
      `contract_state` VARCHAR(5) NULL,
      PRIMARY KEY (`wind_code`))
    ENGINE = MyISAM;"""
    cursor.execute(sql)
    db.commit()
#取出所有数据
sql_data=cursor.fetchall()
df = pd.DataFrame(list(sql_data),columns=['wind_code','contract_state'])
df.index = df['wind_code']
#获取数据
s=w.wset("optioncontractbasicinfo",
          "exchange=sse;windcode=510050.SH;status=all;field=wind_code,sec_name,call_or_put,exercise_price,contract_unit,limit_month,listed_date,exercise_date,settlement_date,contract_state")
temp=s
result = pd.DataFrame(s.Data)
result = result.T
result.columns = s.Fields #数据拼接完成
result.index = result['wind_code']
#判断数据是否在sql_data 里面
for code in result.index:
    if code in df.index:
        if df.loc[code]['contract_state'] == '上市' and result.loc[code]['contract_state'] == '退市':
            print('update '+code)
            sql="""update information set contract_state='退市'
                where wind_code = '"""+code+"""';"""
            cursor.execute(sql)
            db.commit()    
        else:
            pass
        result=result.drop(code)
         
pd.io.sql.to_sql(result,'information', yconnect, 
             schema='50etf_option',index=False,if_exists='append')


    
    
    