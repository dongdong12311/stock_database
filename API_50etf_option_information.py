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
class OPTIONINFOR:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","50etf_option",charset='utf8')
        self.__cursor=self.__db.cursor()      
    def readDatas(self,wind_code='',limit_month=''):
        if wind_code != '':
            sql="SELECT * FROM 50etf_option.information where wind_code = '"+wind_code+"';"
        elif limit_month != '':
            sql = "SELECT * FROM 50etf_option.information where limit_month = '"+limit_month+"';"
        else:
            sql = "SELECT * FROM 50etf_option.information ;"
        return self.__fetchall(sql)
    def __fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall())  
    def fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall()) 
    def fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone()) 
    def __fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone())  
        
if __name__=='__main__':
    a=OPTIONINFOR()
    re=a.readDatas(wind_code='10001211')
    re=a.readDatas(limit_month='2017-03')