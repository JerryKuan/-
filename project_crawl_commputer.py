import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random
headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Connection': 'keep - alive',
         'Cookie':'__jsluid=3afb803b861d8200896eace3e92cd8ed; UM_distinctid=15b6a43d26d36d-0929e35c24088f-396b4e08-140000-15b6a43d26e30; stock=sh601398%2Csh600030%2Csz000002%2Csh600547%2Csh601857; fund=fu_000001%2Cfu_000021%2Cfu_162204%2Cfu_162703%2Cfu_260104; ASPSESSIONIDQADRTQTC=HHCHHABBOLEBFAFCPBECOGHA; Hm_lvt_f1cc3b90f5460d50d5200128a455979d=1492236253,1492327254,1493343469,1493362573; Hm_lpvt_f1cc3b90f5460d50d5200128a455979d=1493369329; CNZZDATA596588=cnzz_eid%3D522829458-1492132022-%26ntime%3D1493369161',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
         }
# wb_data=requests.get("http://hao123.cnease.cn/webdir/network/2-1.html",headers=headers)
# soup=BeautifulSoup(wb_data.text,'lxml')
# for i in soup.select(".scatelist li a"):
#     print("'"+i.attrs['href'][:-6],i.text+"',")
list_url=[
'/webdir/internet/21- 互联网',
'/webdir/hardware/23- 硬件',
'/webdir/digital/24- 数码',
'/webdir/software/25- 软件',
'/webdir/computer/26- 电脑',
'/webdir/programming/27- 编程',
'/webdir/design/28- 设计',
'/webdir/buildweb/29- 建站',
'/webdir/search/31- 搜索引擎大全',
'/webdir/website/32- 网址',
'/webdir/blog/33- 博客',
'/webdir/bookmark/34- 网摘',
'/webdir/resource/35- 资源',
'/webdir/chat/38- 聊天',
'/webdir/hacker/39- 黑客',
'/webdir/antivirus/40- 杀毒',
'/webdir/gongju/562- 工具'
]
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()

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
    try:
        url = "http://hao123.cnease.cn/{}{}.html".format(channel, str(page))
        html=requests.get(url,headers=headers,timeout=5)
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
            return True
        else:
            return None
    except Exception as e:
        print("Exception"+str(e))
        return True

for urllist in list_url:
    ul=urllist.split()
    channel=ul[0]
    secondcate=ul[1]
    for page in range(1,1000):
        time.sleep(random.randint(1,5))
        flag=crawlcontent(channel,page,"电脑网络",secondcate)
        if flag is None:
            break
