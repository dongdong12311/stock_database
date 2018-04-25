# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:40:04 2018

@author: Administrator
更新历史数据，open high low close 成交量 持仓量 隐含波动率
为了方便起见，我们只是更新已经 退市的 期权

"""
import pymysql    
import pandas as pd
import os,sys
from sqlalchemy import create_engine  
import numpy as np
import datetime
from WindPy import *
from WindPy import w
from dateutil.parser import parse
from API_50etf_option_information import OPTIONINFOR
w.start()
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/50etf_option?charset=utf8')  
db=pymysql.connect("localhost","root","123123","50etf_option",charset='utf8')
cursor=db.cursor()
a=OPTIONINFOR()
re=pd.DataFrame(list(a.readDatas()))
re.index = re[0]
for code in re.index:
    #判读数据是否存在
    sql="SELECT * FROM 50etf_option.`"+code+"`;"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        sql = """CREATE TABLE  50etf_option.`"""+code+"""`(
              `CODE` VARCHAR(20) NOT NULL,
              `DATE` DATETIME NOT NULL,
              `OPEN` DOUBLE NULL,
              `HIGH` DOUBLE NULL,
              `LOW` DOUBLE NULL,
              `CLOSE` DOUBLE NULL,
              `VOLUME` DOUBLE NULL,
              `OI` INT NULL,
              `US_IMPLIEDVOL` DOUBLE NULL,
              PRIMARY KEY (`DATE`))
        ENGINE = MyISAM;"""
        cursor.execute(sql)
        db.commit()
    sql="SELECT * FROM 50etf_option.`"+code+"`;"
    cursor.execute(sql)
    db.commit()
    temp = cursor.fetchall()
    if len(temp) == 0 and re.loc[code][9] == '退市':
        print("获取 " + code + "  数据")
        wind_code = code + '.SH'
        start = re.loc[code][6]
        end = datetime.strftime(re.loc[code][7].to_pydatetime(),"%Y-%m-%d")
        s = w.wsd(wind_code, "open,high,low,close,volume,oi,us_impliedvol", start, end, "")
        temp=s
        result = pd.DataFrame(s.Data)
        result = result.T
        result.columns = s.Fields #数据拼接完成
        result['CODE']=[code]*len(result)
        result['DATE']=s.Times      
        try:
            pd.io.sql.to_sql(result,code, yconnect, 
                         schema='50etf_option',index=False,if_exists='append')
        except:
            print(code)
            print("无法写入")