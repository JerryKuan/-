#将抓取的URL内容信息分词后保存到txt文本中
import pymysql
import jieba
conn=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='web_repository',charset='utf8')
cur=conn.cursor()
cur.execute("SELECT content from url_category where firstcategory='生活服务' ")
all=cur.fetchall()

#count=6738

def WriteToTxt(content):
    #global count
    #stopkeyword=[line.strip() for line in open(r'C:\Users\13693\Desktop\实训\test\stopword.txt',encoding='utf-8').readlines()]
    #stopkeyword.extend("　")
    #stopkeyword.extend(" ")

    currentfile = "C://Users//13693//Desktop//实训//test//stopword_done4.txt"
    fsave = open(currentfile, 'a+', encoding='utf-8')
    seg=jieba.cut(content.strip(),cut_all=False)
    #for i in seg:
        #if i  in stopkeyword and i.isdigit()==False:
            #fsave.write(i+" ")
    for i in seg:

        print(i,end=' ')
        fsave.write(i+" ")
    #count+=1
    #fsave.close()

for i in all:
    #print(i[0])
    WriteToTxt(i[0])
cur.close()
conn.close()
