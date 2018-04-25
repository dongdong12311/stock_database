import pymysql
class TDays:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","tdays",charset='utf8')
        self.__cursor=self.__db.cursor()
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
        return self.__fetchall(sql)
        return self.__fetchone(sql)
    def __fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall())  
    def __fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone())  
if __name__=='__main__':
    a=TDays()
    re=a.GetTradeDays()
    re=a.GetTradeDays('2018-01-01')
    re=a.GetTradeDays('2018-01-01','2018-01-30')