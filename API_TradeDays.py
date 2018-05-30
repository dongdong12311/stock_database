import pymysql
from stock_database.SqlHandle import SqlHandle
class TDays(SqlHandle):
    def __init__(self):
        self.db=pymysql.connect("localhost","root","123123","tdays",charset='utf8')
        self.cursor=self.db.cursor()
    def GetTradeDays(self,*args):
        if len(args)==0:
            sql="SELECT * FROM tdays.tdays;"
        elif len(args)==1:
            sql="SELECT * FROM tdays.tdays where date >= '"+args[0]+"';"
        elif len(args)==2:
            sql="SELECT * FROM tdays.tdays where date >= '"+args[0]+"' and date<'"+args[1]+"';"
        else:
            print('wrong input in getdays()!')
            return None
        return self.fetchall(sql)

    def GetTradeDays_Include_end(self,*args):
        if len(args)==0:
            sql="SELECT * FROM tdays.tdays;"
        elif len(args)==1:
            sql="SELECT * FROM tdays.tdays where date >= '"+args[0]+"';"
        elif len(args)==2:
            sql="SELECT * FROM tdays.tdays where date >= '"+args[0]+"' and date<='"+args[1]+"';"
        else:
            print('wrong input in getdays()!')
            return None
        return self.fetchall(sql)

if __name__=='__main__':
    a=TDays()
    re=a.GetTradeDays()
    re=a.GetTradeDays('2018-01-01')
    re=a.GetTradeDays('2018-01-01','2018-01-30')