import tushare as ts
import pymysql
from  API_IpoDate import IpodateManagement
from dateutil.parser import parse
import datetime
ipodates=IpodateManagement()
db=pymysql.connect("localhost","root","123123","ipodate",charset='utf8')
cursor=db.cursor()
a=ts.get_stock_basics()
allcodes=list(a.index)
for code in allcodes:
    try:
        ipodate=ipodates.GetIpodate(code)[1]
    except:
        print(code+"is not exist")
        sql="insert into ipodate values('"+code+"','"+'2050-010-01'+"');"    
        cursor.execute(sql)
        db.commit()
        ipodate=ipodates.GetIpodate(code)[1]
    ipostr=datetime.datetime.strftime(ipodate,"%Y%m%d")
    if int(a.loc[code]['timeToMarket'])!=0:
        if ipostr!=str(int(a.loc[code]['timeToMarket'])):
            print("更新"+code+"ipodate")
            sql="""update ipodate set date='"""+datetime.datetime.strftime(parse(str(int(a.loc[code]['timeToMarket']))),"%Y-%m-%d")+"""'
                where stock = '"""+code+"""';"""
            cursor.execute(sql)
            db.commit()    
print("数据更新完毕")
