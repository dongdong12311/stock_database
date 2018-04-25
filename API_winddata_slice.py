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
class WindData_sliceDB:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","stockslice",charset='utf8')
        self.__cursor=self.__db.cursor()      
    def readData(self,date):
        sql="SELECT * FROM stockslice.`"+date+"`;"
        return self.__fetchall(sql)
    def GetcolumnNames(self):
        return ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHG', 'PCT_CHG',
               'ADJFACTOR', 'TURN', 'VOL_RATIO', 'INDUSTRY_CSRC12', 'FREE_TURN',
               'PE_TTM', 'PB_LF', 'CODE']
    def __fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall())  
    def __fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone())  
        
if __name__=='__main__':
    a=WindData_sliceDB()
    re2=a.readData('2017-01-04')
    re=a.GetcolumnNames()