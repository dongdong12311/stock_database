# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 21:19:39 2018

@author: Administrator
"""
import pymysql    
from SqlHandle import SqlHandle
class WindDataDB(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","stock",charset='utf8')
        self.cursor=self.db.cursor()      
    def readDatas(self,code,*args):
        if len(args)==0:
            sql="SELECT * FROM stock."+code+";"
        elif len(args)==1:
            sql="SELECT * FROM stock."+code+" where date >= '"+args[0]+"';"
        elif len(args)==2:
            sql="SELECT * FROM stock."+code+" where date >= '"+args[0]+"' and date<'"+args[1]+"';"
        else:
            print('wrong input in getdays()!')
            return None
        return self.fetchall(sql)
    def readData(self,code,date):
        sql="SELECT * FROM stock."+code+" where date = '"+date+"';"
        return self.fetchall(sql)

        
if __name__=='__main__':
    a=WindDataDB()
    re1=a.readDatas('600232','2010-01-01','2017-01-01')
    re2=a.readData('600232','2017-01-04')