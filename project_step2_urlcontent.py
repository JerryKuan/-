import pymysql
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
# import pymongo
# import re
# client=pymongo.MongoClient("localhost",27017)
# webtest=client['webtest']
# webdata_test=webtest['webdata_test']
# n=re.compile('www.baidu.com')
#
# for i in webdata_test.find({"result.url":n}).limit(100):
#     print(i)

conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
cur.execute("select id,url from url_category ")
allurl=cur.fetchall()
# for i in allurl:
#     print(i[0])
headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Connection': 'keep - alive',
         'Cookie':'__jsluid=3afb803b861d8200896eace3e92cd8ed; UM_distinctid=15b6a43d26d36d-0929e35c24088f-396b4e08-140000-15b6a43d26e30; stock=sh601398%2Csh600030%2Csz000002%2Csh600547%2Csh601857; fund=fu_000001%2Cfu_000021%2Cfu_162204%2Cfu_162703%2Cfu_260104; ASPSESSIONIDQADRTQTC=HHCHHABBOLEBFAFCPBECOGHA; Hm_lvt_f1cc3b90f5460d50d5200128a455979d=1492236253,1492327254,1493343469,1493362573; Hm_lpvt_f1cc3b90f5460d50d5200128a455979d=1493369329; CNZZDATA596588=cnzz_eid%3D522829458-1492132022-%26ntime%3D1493369161',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
         }
def getUrlCoding(data):  # 解决网站的编码问题
    charset='utf-8'
    if data.encoding.lower()=='utf-8' or data.encoding=='utf8':
        return 'utf-8'
    if data.encoding.lower()=='gb2312':
        return 'gb2312'
    if data.encoding.lower()=='gbk':
        return 'gbk'
    if data.encoding.lower()=='gb18030':
        return 'GB18030'
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(data.text)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    return charset
#url='https://www.baidu.com/s?wd=requests.get参数时间'
def urlsoup(url):
    try:
        wb_data=requests.get(url,headers=headers,timeout=3)
        wb_data.encoding=getUrlCoding(wb_data)
        soup=BeautifulSoup(wb_data.text,'lxml')
        return soup
    except Exception:
        return None
start=datetime.datetime.now()
for i in allurl:
    url="http://"+i[1]
    soup=urlsoup(url)
    anstitle = ""
    anskeywords = ""
    ansdescription = ""
    try:
        if soup is not None:
            title=soup.find('title')
            if title is not None:
                anstitle=title.text
            else:
                anstitle=""
            keywords=soup.find("meta",{"name":"keywords"})
            if keywords is None:
                keywords=soup.find("meta",{"name":"Keywords"})
            if keywords is not None:
                anskeywords=keywords["content"]
            else:
                anskeywords=""
            description=soup.find("meta",{"name":"description"})
            if description is None:
                description=soup.find("meta",{"name":"Description"})
            if description is not None:
                ansdescription=description["content"]
            else:
                ansdescription=""
    except Exception as e:
        print("Exception:"+str(e)+url)
    try:
        #cur.execute("update test_url set title=%s,description=%s,keywords=%s where id=%s",(anstitle,ansdescription,anskeywords,i[0]))
        #cur.execute("update test_url set title='"+anstitle+"',description='"+ansdescription+"',\
        #keywords='"+anskeywords+"' where id="+str(i[0]))
        cur.execute("insert into test_url(title,description,keywords) values('" + anstitle + "','" + ansdescription + "',\
                '" + anskeywords + "')")
        print("url:" + url, "title:" + anstitle, "keywords:" + anskeywords, "description:" + ansdescription)

        #cur.execute("insert into test_url(id,title,description,keywords) values(i[0],anstitle,ansdescription,anskeywords,)");
        conn.commit()
    except Exception as e:
        print("Exception:"+str(e)+url)
end=datetime.datetime.now()
print(end-start)
cur.close()
conn.close()

