#获取股票的名称和代码

import pymysql
from  .SqlHandle import SqlHandle
class CodeManagement(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","wind_stock_data",charset='utf8')
        self.cursor=self.db.cursor()
    def GetCodeName(self):
        sql="SELECT * FROM wind_stock_data.stockname;"
        return self.fetchall(sql)
    def GetWindCode(self):
        sql="SELECT * FROM wind_stock_data.stocknamechar;"
        return self.fetchall(sql)
'''
if __name__=='__main__':
    a=CodeManagement()
    codename=a.GetCodeName()
    windcode = a.GetWindCode()'''