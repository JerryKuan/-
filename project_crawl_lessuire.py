#娱乐休闲 9000+
import requests
from bs4 import BeautifulSoup
import pymysql
import time
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
headers={
    'Connection':'Keep-Alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
#wb_data=requests.get("http://www.yahoo001.com/webdir/entertainment/1/ctime/123123123",headers=headers)
#soup=BeautifulSoup(wb_data.text,'lxml')
# for i in soup.find('div',{'id':'subcate'}).findAll("a"):
#     print(i.attrs['href'],i.text)
#list_url=#['/webdir/music/6/ctime/ 音乐',
#'/webdir/video/7/ctime/ 影视',
#'/webdir/game/8/ctime/ 游戏',
#'/webdir/animation/9/ctime/ 动漫',
#'/webdir/picture/10/ctime/ 图片',
#'/webdir/fiction/11/ctime/ 小说',
#'/webdir/joke/12/ctime/ 笑话',
list_url=['/webdir/astrology/13/ctime/ 星相',
'/webdir/make-friends/14/ctime/ 交友',
'/webdir/news/15/ctime/ 新闻',
'/webdir/sport/16/ctime/ 体育',
'/webdir/military/17/ctime/ 军事',
'/webdir/photography/18/ctime/ 摄影',
'/webdir/star/19/ctime/ 明星',
'/webdir/community/20/ctime/ 社区',
'/webdir/chat/38/ctime/ 聊天']

# for url in list_url:
#     print(url.split()[1])
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
        time.sleep(1)
        flag=crawlcontent(channel,page,"休闲娱乐",secondcate)
        if flag is None:
            break

cur.close()
conn.close()
