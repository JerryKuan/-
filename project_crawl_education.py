#娱乐休闲 9000+
import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
headers={
    'Connection':'Keep-Alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
# wb_data=requests.get("http://www.yahoo001.com/webdir/culture/4/ctime/1",headers=headers)
# soup=BeautifulSoup(wb_data.text,'lxml')
# for i in soup.find('div',{'id':'subcate'}).findAll("a"):
#     print("'"+i.attrs['href'][:-1],i.text+"',")

list_url=[
'/webdir/education/66/ctime/ 教育',
'/webdir/knowledge/67/ctime/ 知识',
'/webdir/yuyan/68/ctime/ 语言',
'/webdir/exam/69/ctime/ 考试',
'/webdir/paper/70/ctime/ 论文',
'/webdir/xuexiao/71/ctime/ 学校',
'/webdir/campus/72/ctime/ 校园',
'/webdir/library/73/ctime/ 图书馆',
'/webdir/overseas/74/ctime/ 出国留学',
'/webdir/folkart/75/ctime/ 曲艺',
'/webdir/hobby/76/ctime/ 爱好',
'/webdir/science/77/ctime/ 科技',
'/webdir/humanities/78/ctime/ 人文',
'/webdir/religion/79/ctime/ 宗教',
'/webdir/welfare/80/ctime/ 公益',
'/webdir/xuexi/725/ctime/ 学习'
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

        return True
    else:
        return None

for urllist in list_url:
    ul=urllist.split()
    channel=ul[0]
    secondcate=ul[1]
    for page in range(1,1000):
        time.sleep(random.randint(1,5))
        flag=crawlcontent(channel,page,"文化教育",secondcate)
        if flag is None:
            break

cur.close()
conn.close()
