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
from dateutil.parser import parse
class tushareData_sliceDB:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","tusharedataslice",charset='utf8')
        self.__cursor=self.__db.cursor()      
    def readData(self,date):
        sql="SELECT * FROM tusharedataslice.`"+date+"`;"
        return self.__fetchall(sql)
    def GetcolumnNames(self):
        return ['date', 'open', 'high', 'low', 'close', 'volume', 'price_change',
                           'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5',
                           'v_ma10', 'v_ma20', 'turnover']
    def __fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall())  
    def __fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone())  
        
if __name__=='__main__':
    a=tushareData_sliceDB()
    re2=a.readData('2015-01-05')
    re=a.GetcolumnNames()