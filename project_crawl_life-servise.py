#娱乐休闲 9000+
import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
# wb_data=requests.get("http://www.yahoo001.com/webdir/life-service/3/ctime/1",headers=headers)
# soup=BeautifulSoup(wb_data.text,'lxml')
# for i in soup.find('div',{'id':'subcate'}).findAll("a"):
#     print("'"+i.attrs['href'],i.text+"',")
# list_url=[
# '/webdir/shopping/41/ctime/ 购物',
# '/webdir/lottery/42/ctime/ 彩票',
# '/webdir/traffic/44/ctime/ 交通',
# '/webdir/stock/45/ctime/ 股票',
# '/webdir/fund/46/ctime/ 基金',
# list_url=['/webdir/bank/47/ctime/ 银行',
# '/webdir/insurance/48/ctime/ 保险',
# '/webdir/house/49/ctime/ 房产',
# '/webdir/car/50/ctime/ 汽车',
# '/webdir/television/51/ctime/ 电视',
# '/webdir/mobile/52/ctime/ 手机',
# '/webdir/communication/53/ctime/ 通信',
# '/webdir/healthy/54/ctime/ 健康',
# '/webdir/food/55/ctime/ 美食',
# list_url=['/webdir/pet/56/ctime/ 宠物',
# '/webdir/children/57/ctime/ 儿童',
# '/webdir/female/58/ctime/ 女性',
# '/webdir/fashion/59/ctime/ 时尚',
# '/webdir/tourism/60/ctime/ 旅游',
# '/webdir/life/61/ctime/ 生活',
# '/webdir/brand/62/ctime/ 品牌',
# '/webdir/recruitment/64/ctime/ 招聘',
# '/webdir/law/65/ctime/ 法律',
# '/webdir/laonian/753/ctime/ 老年',
# ]
list_url=[
'/webdir/tourism/60/ctime/ 旅游',
'/webdir/life/61/ctime/ 生活',
]

cur.execute("select url from url_category")
allurl=cur.fetchall()
urlset=set()
for u in allurl:
    urlset.add(u[0])

def insertUrl(url,firstcategory,secondcategory,content):#插入一条url
    cur.execute("select*from url_category where url=%s",url)
    if cur.rowcount==0:
        cur.execute("insert into url_category(url,firstcategory,secondcategory,content) values (%s,%s,%s,%s)",(url,firstcategory,secondcategory,content))
        conn.commit()
def crawlcontent(channel,page,firstcate,secondcate):
    url = "http://www.yahoo001.com{}{}".format(channel, str(page))
    html=requests.get(url,headers=headers)
    soup=BeautifulSoup(html.text,'lxml')
    if soup.find("div",{"class":"info"}):#该页有内容
        link = soup.select('.info address a.visit')
        content = soup.select('.info p')
        for c, l in zip(content, link):
            savecontent=c.text#要保存的URL
            saveurl=l['href'].replace('http://','').replace('https://','')#要保存的内容
            print(channel+str(page)+saveurl)
            if saveurl not in urlset:
                insertUrl(saveurl,firstcate,secondcate,savecontent)
        #page+=1
        #crawlcontent(channel, page, firstcate, secondcate)
        return True
    else:
        return None

#for urllist in list_url:
ul=list_url[1].split()
channel=ul[0]
secondcate=ul[1]
for page in range(1,1000):
    #time.sleep(random.randint(1,10))
    time.sleep(1)
    flag=crawlcontent(channel,page,"生活服务",secondcate)
    if flag is None:
        break




cur.close()
conn.close()
