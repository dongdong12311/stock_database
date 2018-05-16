#获取股票的名称和代码

import pymysql
from  SqlHandle import SqlHandle
class CodeManagement(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","stock",charset='utf8')
        self.cursor=self.db.cursor()
    def GetCodeName(self):
        sql="SELECT * FROM stock.stockname;"
        return self.fetchall(sql)
    def GetWindCode(self):
        sql="SELECT * FROM stock.stocknamechar;"
        return self.fetchall(sql)

if __name__=='__main__':
    a=CodeManagement()
    re=a.GetCodeName()