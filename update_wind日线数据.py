# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 21:19:39 2018

@author: Administrator
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
from API_StockCode import CodeManagement
w.start()
codes=CodeManagement().GetCodeName()
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/stock?charset=utf8')  
db=pymysql.connect("localhost","root","123123","stock",charset='utf8')
cursor=db.cursor()
for code in codes:
    code=code[0]
    if code.startswith('6'):
        windcode=code+'.SH'
    else:
        windcode=code+'.SZ'        
    
    
    sql="""SELECT * FROM stock.`"""+code+"""` 
    order by DATE desc limit 1;"""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        sql = """CREATE TABLE  `stock`.`"""+code+"""` (
          `DATE` DATETIME NOT NULL,
          `OPEN` DOUBLE NULL,
          `HIGH` DOUBLE NULL,
          `LOW` DOUBLE NULL,
          `CLOSE` DOUBLE NULL,
          `CHG` DOUBLE NULL,
          `PCT_CHG` DOUBLE NULL,
          `ADJFACTOR` DOUBLE NULL,
          `TURN` DOUBLE NULL,
          `VOL_RATIO` DOUBLE NULL,
          `INDUSTRY_CSRC12` VARCHAR(45) NULL,
          `FREE_TURN` DOUBLE NULL,
          `PE_TTM` DOUBLE NULL,
          `PB_LF` DOUBLE NULL,
          `CODE`  VARCHAR(10) NULL,
          PRIMARY KEY (`DATE`))
        ENGINE = MyISAM;"""
        cursor.execute(sql)
        db.commit()
    try:
        temp=cursor.fetchall()[0][0]
    except:
        temp=parse('2017-11-01')
    #获取日期
    tomorrorw=temp+timedelta(1)
    if  datetime.today().hour>=16:
        todaytime=datetime.today()
    else:
        todaytime=datetime.today()-timedelta(1)
    today=datetime.strftime(todaytime,'%Y-%m-%d')
    if tomorrorw>todaytime:
        print("数据不需要更新")
        continue     
    ipo=datetime.strftime(tomorrorw,'%Y-%m-%d')
    print('正在更新 '+code+ ' 的数据 ','更新的日期从 '+ipo+' 开始')
    s=w.wsd(windcode, 
    "open,high,low,close,chg,pct_chg,adjfactor,turn,vol_ratio,industry_CSRC12,free_turn,pe_ttm,pb_lf",
    ipo, today,
    "VolumeRatio_N=5;industryType=1")
    temp=s
    result = pd.DataFrame(s.Data)
    result.columns=s.Times
    result = result.T
    result.columns = s.Fields
    result['CODE']=s.Codes*len(result)
    temp=result
    temp['DATE']=temp.index      
    try:
        pd.io.sql.to_sql(temp,code, yconnect, 
                     schema='stock',index=False,if_exists='append')
    except:
        print(code)
        print("无法写入")
        

