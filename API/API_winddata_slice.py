# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 21:19:39 2018

@author: Administrator
"""

from .SqlHandle import SqlHandle
import pymysql 
class WindData_sliceDB(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","wind_stock_data_slice",charset='utf8')
        self.cursor=self.db.cursor()      
    def readData(self,date):
        sql="SELECT * FROM wind_stock_data_slice.`"+date+"`;"
        return self.fetchall(sql)
    def GetcolumnNames(self):
        return ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHG', 'PCT_CHG',
               'ADJFACTOR', 'TURN', 'VOL_RATIO', 'INDUSTRY_CSRC12', 'FREE_TURN',
               'PE_TTM', 'PB_LF', 'CODE']

'''        
if __name__=='__main__':
    a=WindData_sliceDB()
    re2=a.readData('2017-01-04')
    re=a.GetcolumnNames()'''