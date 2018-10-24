# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 21:19:39 2018

@author: Administrator
"""
import pymysql    
from datetime import datetime
import datetime
from  .SqlHandle import SqlHandle
class OPTIONINFOR(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","50etf_option",charset='utf8')
        self.cursor=self.db.cursor()      
    def readDatas(self,wind_code='',limit_month=''):
        if wind_code != '':
            sql="SELECT * FROM 50etf_option.information where wind_code = '"+wind_code+"';"
        elif limit_month != '':
            sql = "SELECT * FROM 50etf_option.information where limit_month = '"+limit_month+"';"
        else:
            sql = "SELECT * FROM 50etf_option.information ;"
        return self.fetchall(sql)

