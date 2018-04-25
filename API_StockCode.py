import pymysql
class CodeManagement:
    def __init__(self):
        self.__db=pymysql.connect("localhost","root","123123","stock",charset='utf8')
        self.__cursor=self.__db.cursor()
    def GetCodeName(self):
        sql="SELECT * FROM stock.stockname;"
        return self.__fetchall(sql)
    def GetWindCode(self):
        sql="SELECT * FROM stock.stocknamechar;"
        return self.__fetchall(sql)
    def __fetchall(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchall())  
    def __fetchone(self,sql):
        self.__cursor.execute(sql)
        self.__db.commit()
        return (self.__cursor.fetchone())  
if __name__=='__main__':
    a=CodeManagement()
    re=a.GetCodeName()