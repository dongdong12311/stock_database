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
from datetime import datetime
import datetime
from WindPy import *
from WindPy import w
global temp
temp=[]
w.start()
from dateutil.parser import parse
yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/stock_index?charset=utf8')  
db=pymysql.connect("localhost","root","123123","stock_index",charset='utf8')
cursor=db.cursor()

index_name={"上证50":"000016.SH",
            "50etf":"510050.SH",
            "上证综指":"000001.SH",
            "深圳综指":"399106.SZ"}

def create(index_name):
    #创建指数的数据
    sql = """CREATE TABLE  `stock_index`.`"""+index_name+"""` (
          `DATE` DATETIME NOT NULL,
          `OPEN` DOUBLE NULL,
          `HIGH` DOUBLE NULL,
          `LOW` DOUBLE NULL,
          `CLOSE` DOUBLE NULL,
          `VOLUME` DOUBLE NULL,
          `AMT` DOUBLE NULL,
          `VOL_RATIO` DOUBLE NULL,
          PRIMARY KEY (`DATE`))
        ENGINE = MyISAM;"""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(index_name+" already exists")
def UpdateData(index_name):
    global temp
    sql="""SELECT * FROM stock_index.`"""+index_name+"""` 
    order by DATE desc limit 1;"""
    today=datetime.today()
    todaystr=datetime.strftime(today,"%Y-%m-%d")
    try:
        cursor.execute(sql)
        db.commit()
        startDate=cursor.fetchall()[0][0]+timedelta(1)
    except:
        print(index_name+" 数据集不存在，初始化日期为1992-01-01")
        startDate=datetime(1992,1,1)
    startDatestr=datetime.strftime(startDate,"%Y-%m-%d")
    #得到年末的时间
    endDate=datetime(startDate.year,12,31)
    endDatestr=datetime.strftime(endDate,"%Y-%m-%d")
    isNottheEnd=True
    while isNottheEnd:
        if endDate<today:
            temp=w.wsd(index_name, "open,high,low,close,volume,amt,vol_ratio",
               startDatestr,endDatestr, "VolumeRatio_N=5")
            startDate=datetime(startDate.year+1,1,1)
            startDatestr=datetime.strftime(startDate,"%Y-%m-%d")
            endDate=datetime(startDate.year,12,31)
            endDatestr=datetime.strftime(endDate,"%Y-%m-%d")
        else:
            temp=w.wsd(index_name, "open,high,low,close,volume,amt,vol_ratio",
               startDatestr,todaystr, "VolumeRatio_N=5")
            isNottheEnd=False
        result = pd.DataFrame(temp.Data)
        result.columns=temp.Times
        result = result.T
        result.columns = temp.Fields
        result=result.dropna()
        result['DATE']=result.index
        if result.size>0:
            pd.io.sql.to_sql(result,index_name, yconnect, 
                 schema='stock_index',index=False,if_exists='append')            
        
    



for name,index in index_name.items():
    create(index)
    UpdateData(index)
