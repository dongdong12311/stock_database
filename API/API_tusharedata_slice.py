# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 21:19:39 2018

@author: Administrator
"""
import pymysql 
from  .SqlHandle import SqlHandle
class tushareData_sliceDB(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","tushare_stock_data_slice",charset='utf8')
        self.cursor=self.db.cursor()      
    def readData(self,date):
        sql="SELECT * FROM tushare_stock_data_slice.`"+date+"`;"
        return self.fetchall(sql)
    def GetcolumnNames(self):
        return ['date', 'open', 'high', 'low', 'close', 'volume', 'price_change',
                           'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5',
                           'v_ma10', 'v_ma20', 'turnover']

'''        
if __name__=='__main__':
    a=tushareData_sliceDB()
    re2=a.readData('2017-01-05')
    re=a.GetcolumnNames()'''