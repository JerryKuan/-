#对URL按一定规则切分，使用分类算法或数据库比对确定URL类别
import requests
from bs4 import BeautifulSoup
import re
import time
import pymongo
import pymysql
import re
from multiprocessing import Pool
import datetime
#from all_test.classify_demo import JudgeCate
from project_step_Fun2_classify_update import JudgeCate
client=pymongo.MongoClient("localhost",27017)
webtest=client['webtest']
webdata=webtest['webdata']

conn=pymysql.connect(host='localhost',port=3306,db='web_repository',user='root',password='root',charset='utf8')
cur=conn.cursor()
cur.execute("select url from url_category")

urlset=set()
allurl=cur.fetchall()
for u in allurl:
   urlset.add(u[0])

def insertUrl(url,category):
   #cur.execute("insert into url_repository(url,category) values(%s,%s)",(url,category))
   cur.execute("insert into url_repository(url,category) values('" + url + "', '" + category + "')")
   conn.commit()

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
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(data.text)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    return charset

def urlsoup(url):
    try:
        wb_data=requests.get(url,headers=headers,timeout=3)
        if wb_data.status_code != 200:
            return None
        wb_data.encoding=getUrlCoding(wb_data)
        soup=BeautifulSoup(wb_data.text,'lxml')
        return soup
    except Exception:
        return None

def deletefileextension(url):#删除要下载的文件后缀
    url = url.replace("http://", '')
    if '/' in url:#如果当前URL有路径，才可能存在文件后缀
        houzhui = url.split('.')#文件有后缀，才一定存在.文件后缀
        houzhui = houzhui[len(houzhui) - 1]
        if len(houzhui) <= 7:#文件后缀的长度一定小于7
            split = url.split('/')#删除文件包含文件后缀的最后一个路径
            url = url.replace(split[len(split) - 1], '')
            url=url[:-1]#删除文件/
    return url


def cral_content(url,id):
    url="http://"+url
    soup=urlsoup(url)
    anstitle = "null"
    anskeywords = "null"
    ansdescription = "null"
    try:
        if soup is not None:
            title=soup.find('title')
            if title is None:
                return False
            else:
                anstitle=title.text.replace('\n','').replace('\r','').replace('\t','')
                if anstitle == "None" or anstitle == "Untitled Page" or '404' in anstitle or '报错页面' in anstitle or '页面不存在' in anstitle or anstitle=="":
                    return False
            keywords=soup.find("meta",{"name":"keywords"})
            if keywords is None:
                keywords=soup.find("meta",{"name":"Keywords"})
            if keywords is not None:
                anskeywords=keywords["content"]
            else:
                anskeywords="null"
            description=soup.find("meta",{"name":"description"})
            if description is None:
                description=soup.find("meta",{"name":"Description"})
            if description is not None:
                ansdescription=description["content"]
            else:
                ansdescription="null"
            Info={'title':anstitle,'description':ansdescription,'keywords':anskeywords,'url':url}
            print("url:"+url,"title:"+anstitle,"keywords:"+anskeywords,"description:"+ansdescription)
            #通过朴素贝叶斯算法判断该URL的类别
            content=""
            if anstitle!='null':
                content+=anstitle
            if ansdescription!='null':
                content+=ansdescription
            if anskeywords!='null':
                content+=anskeywords
            cate=JudgeCate(content)
            #更新
            if url not in urlset:
                if len(url)<254:
                    url=url[7:]
                    insertUrl(url, cate)
                    urlset.add(url)

            webdata.update({'_id': id}, {'$set':{'data': str(Info),'NBMtype':cate}})  # 更新到Mongodb中
            return Info
    except Exception as e:
        print("Exception:" + str(e) + url)
        return False



def FirstSplit(url):#按照/切分，每次删除最后一个路径
    spliturl=url.split('/')
    #url=url.replace(spliturl[len(spliturl)-1],'')error
    url=url[:-len(spliturl[len(spliturl)-1])-1]
    return url
def SecondSplit(url):#按照.切分，每个删除最前的一个域名
    spliturl=url.split('.')
    #url=url.replace(spliturl[0],'')error
    url=url[len(spliturl[0])+1:]
    return url
def judge_url_in_repository(url,id):
    cur.execute("select category from url_repository where url like %s limit 1", ('%' + url + '%'))
    if cur.rowcount != 0:
        print(id,url)
        return cur.fetchone()[0]
def Update_Cate(id,category):#更新数据库类别
    webdata.update({'_id': id}, {'$set': {'NBMtype': category}})
def SplitMain_matchsql(info):#和数据库中URL匹对确定类别
    url=info['result']['url']
    url = deletefileextension(url)
    cate=judge_url_in_repository(url,info['_id'])
    if cate:
        Update_Cate(info['_id'],cate)
        return True
    while '/' in url:#先按照/切分
        url=FirstSplit(url)
        cate=judge_url_in_repository(url,info['_id'])
        if cate:
            Update_Cate(info['_id'], cate)
            return True
    while len(url.split('.'))>2:#再按照'.'切分
        url=SecondSplit(url)
        cate=judge_url_in_repository(url,info['_id'])
        if cate:
            Update_Cate(info['_id'], cate)
            return True
def SplitMain_match_crawl(info):#根据响应服务获取url中的内容确定类别
    url=info['result']['url']
    url = deletefileextension(url)
    if cral_content(url,info['_id']):
        return True
    while '/' in url:#先按照/切分
        url=FirstSplit(url)
        if cral_content(url,info['_id']):
            return True
    while len(url.split('.'))>2:
        url=SecondSplit(url)
        if cral_content(url,info['_id']):
            return True
def Main(info):
    try:
        if SplitMain_matchsql(info)!=True:
            #print('None')
            #数据库中无法匹配则进行爬取
            if SplitMain_match_crawl(info)!=True:
                print('None')
                webdata.update({'_id': info['_id']}, {'$set': {'data': 'None'}})  # 更新到Mongodb中
    except Exception as e:
        print("Exception:"+str(e)+str(info['result']['url']))
if __name__=="__main__":
    start = datetime.datetime.now()
    pool = Pool()  # 多进程，自动分配进程数
    pool.map(Main, [info for info in webdata.find({'$and':[{'NBMtype':{'$exists':False}},{'data':{'$nin':['None']}}]},no_cursor_timeout=True)])
    # for info in webdata_test.find(no_cursor_timeout=True).limit(10):
    #     Main(info)
    end=datetime.datetime.now()
    print(end-start)
    pool.close()
    cur.close()
    conn.close()
