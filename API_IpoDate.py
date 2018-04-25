import pymysql
class IpodateManagement:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","ipodate",charset='utf8')
        self.__cursor=self.__db.cursor()
    def GetIpodate(self,code):
        sql="""SELECT * FROM ipodate.ipodate
        where stock='"""+code+"""';"""
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
    a=IpodateManagement()
    re=a.GetIpodate('600232')