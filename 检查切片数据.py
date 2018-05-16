# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:13:56 2018
不知道为啥，数据库少了一天的切片数据
检查缺少的数据并且补充
@author: Administrator
"""

from API_TradeDays import TDays
from API_StockCode import CodeManagement
from API_IpoDate import IpodateManagement
import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from dateutil.parser import parse
#sql连接
import sys
from API_winddata import WindDataDB
from API_tusharedata import tushareDataDB


class CheckEngine:
    def __init__(self,database):
        self.schema = database
        self.db=pymysql.connect("localhost","root","123123",database,charset='utf8')  
        self.cursor=self.db.cursor()  
        self.tdays=TDays()
    def __fetchall(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor.fetchall()

    def check(self):  
        res = []
        print("检查"+self.schema+"切片数据")
        sql="""show tables"""
        print("正在获取数据")
        re=self.__fetchall(sql)
        start = re[0][0]
        end = re[-1][0]
        tradedays = self.tdays.GetTradeDays_Include_end(start,end)
        td = list(tradedays)
        re=list(re)
        for date  in td :
            temp = (datetime.datetime.strftime(date[0],"%Y-%m-%d"),)
            if temp not in re:
                print(temp,end='')
                print(" 不存在")
                datestr = temp[0]
                res.append(datestr)
        return res 
        
        
        
        
class update_slice_db:
    def __init__(self,dbname): 
        self.schema = dbname
        a=CheckEngine(self.schema)
        self.res = a.check()
        if dbname == 'tusharedataslice':
            self.db = tushareDataDB()
        elif dbname =='stockslice':
            self.db = WindDataDB()
        else:
            print("数据库不存在")
            return  -1
        codesM=CodeManagement()
        self.codes=codesM.GetCodeName()
        self.ipodates=IpodateManagement()
        self.yconnect=create_engine('mysql+mysqldb://root:123123@localhost:3306/'+self.schema+'?charset=utf8')  
    def updatedata(self,datestr):
        stocks={}
        for code in self.codes:
            code=code[0]
            ipodate=self.ipodates.GetIpodate(code)[1]
            if ipodate<parse(datestr):
                print("读取"+code+"数据")
                s=list(self.db.readData(code,datestr))
                if (len(s)>0):
                    s=pd.DataFrame(s)
                    s.index=s[0]
                    s.columns=['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHG', 'PCT_CHG',
                                   'ADJFACTOR', 'TURN', 'VOL_RATIO', 'INDUSTRY_CSRC12', 'FREE_TURN',
                                   'PE_TTM', 'PB_LF', 'CODE']
                    stocks[code]=s
        date = parse(datestr)
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
            self.__write(datestr,dataslice)

    def __write(self,datestr,dataslice):
        print("写入"+datestr)
        pd.io.sql.to_sql(dataslice,datestr, self.yconnect, 
                         schema=self.schema,index=False,if_exists='append')        
name = 'tusharedataslice'
a=CheckEngine(name)
res =  a.check()
s= update_slice_db(name)
try:
    data  = s.updatedata(res[0])
except:
    pass