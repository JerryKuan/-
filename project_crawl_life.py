#娱乐休闲 9000+
import requests
from bs4 import BeautifulSoup
import pymysql
import time
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
# wb_data=requests.get("http://www.yahoo001.com/webdir/computer-network/2/ctime/1",headers=headers)
# soup=BeautifulSoup(wb_data.text,'lxml')
# for i in soup.find('div',{'id':'subcate'}).findAll("a"):
#     print(i.attrs['href'],i.text)
list_url=[
'/webdir/internet/21/ctime/ 互联网',
'/webdir/hardware/23/ctime/ 硬件',
'/webdir/digital/24/ctime/ 数码',
'/webdir/software/25/ctime/ 软件',
'/webdir/computer/26/ctime/ 电脑',
'/webdir/programming/27/ctime/ 编程',
'/webdir/design/28/ctime/ 设计',
'/webdir/buildweb/29/ctime/ 建站',
'/webdir/webmaster/30/ctime/ 站长',
'/webdir/search/31/ctime/ 搜索',
'/webdir/website/32/ctime/ 网址',
'/webdir/blog/33/ctime/ 博客',
'/webdir/yingxiao/34/ctime/ 营销',
'/webdir/resource/35/ctime/ 资源',
'/webdir/desktop/36/ctime/ 桌面',
'/webdir/shejiao/37/ctime/ 社交',
'/webdir/anquan/40/ctime/ 安全',
'/webdir/ad/282/ctime/ 广告',
'/webdir/weixiu/619/ctime/ 维修',
'/webdir/moban/701/ctime/ 模板'
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

for urllist in list_url:
    ul=urllist.split()
    channel=ul[0]
    secondcate=ul[1]
    for page in range(1,1000):
        time.sleep(3)
        flag=crawlcontent(channel,page,"电脑网络",secondcate)
        if flag is None:
            break

cur.close()
conn.close()
