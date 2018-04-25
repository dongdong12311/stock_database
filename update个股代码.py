import tushare as ts
import pymysql
from  API_StockCode import CodeManagement
codes=CodeManagement().GetCodeName()
a=ts.get_stock_basics()
import sys
if len(codes)<len(a):
    print("开始更新数据，需要更新%d个数据"%(len(a)-len(codes)))
    temp=[]
    for code in codes:
        temp.append(code[0])  
    allcodes=list(a.index)
    db=pymysql.connect("localhost","root","123123","stock",charset='utf8')
    cursor=db.cursor()
    for code in allcodes:
        if code not in temp:
            print("加入 code "+code)
            stockname=code
            if code.startswith('6'):
                charstockname='SH'+code
                stocknamechar=code+'SH'
            else:
                charstockname='SZ'+code
                stocknamechar=code+'SZ'
            sql="insert into stockname values('"+code+"');"
            cursor.execute(sql)
            db.commit()
            sql="insert into charstockname values('"+charstockname+"');"
            cursor.execute(sql)
            db.commit()
            sql="insert into stocknamechar values('"+stocknamechar+"');"
            cursor.execute(sql)
            db.commit()          
print("数据更新完毕")
