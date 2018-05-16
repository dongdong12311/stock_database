import pymysql
from SqlHandle import SqlHandle
class IpodateManagement(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","ipodate",charset='utf8')
        self.cursor=self.db.cursor()
    def GetIpodate(self,code):
        sql="""SELECT * FROM ipodate.ipodate
        where stock='"""+code+"""';"""
        return self.fetchone(sql)

if __name__=='__main__':
    a=IpodateManagement()
    re=a.GetIpodate('600232')