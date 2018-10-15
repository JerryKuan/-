from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
'''from all_test.classify_demo import JudgeCate
import pymysql
conn=pymysql.connect(host='localhost',port=3306,db='web_repository',user='root',charset='utf8')
cur=conn.cursor()
cur.execute("select id,title,description,keywords from  test_url where title is not null and title!='' and title not like '%404%' and title not like '%�%' and title not like '%403 Forbidden%' and title not like '%Not Found%' and nbmjudgefirstcategorybycontent is null")
allurl=cur.fetchall()
if __name__=="__main__":
    print('start')
    try:
        for i in allurl:
            content = ""
            if i[1]!='':
                content+=i[1]+" "
            if i[2]!='':
                content+=i[2]+" "
            if i[3]!='':
                content+=i[3]
            cate=JudgeCate(content)
            print(cate)
            cur.execute("update test_url set nbmjudgefirstcategorybycontent=%s where id=%s",(cate,i[0]))
            conn.commit()
    except Exception as e:
        print("Exception:"+str(e))
    print('end')

    conn.close()
    cur.close()'''
corpus = ["爱 音乐 imusic 中国电信 彩铃网 站 爱 音乐 爱 生活 提供 高 品质音乐 排行榜 音乐 推荐 精选 歌单 音乐 活动 内容 imusic",  # 第一类文本切词后的结果，词之间以空格隔开
          "超低空 部落 E 网 音乐教室 简谱 吉他谱 钢琴谱 乐谱 音乐 资源 相关 音乐 知识 学习 音乐 得力助手 chaodikong",
          '卡拉 ok 歌曲 视频 DVD 歌曲 VCD 歌曲 高清 MV 专业 下载 门户 K 歌 快车 KTV 下载 门户 ktvkg',
          '下载 K 米 点歌 K 米网 手机 KTV 在线 K 歌 专业 评分 快乐 分享 ktvme',
          '网络 K 歌 音效 网 SAM 机架 KX 驱动 官网 一键 电音 K 歌 伴侣 艾肯 声卡 调试 官网 网络 K 歌 音效 网 声卡 调试 官网 by 苦比 青年 QQ',]  # 第二类文本的切词结果
          # "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
          # "我 爱 北京 天安门"]  # 第四类文本的切词结果
vectorizer=CountVectorizer(ngram_range=(1,2))#词语转换为词频矩阵
transformer=TfidfTransformer(smooth_idf=True)#统计每个词语的TF-IDF值
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
aa=vectorizer.fit_transform(corpus)
word=vectorizer.get_feature_names()
weight=aa.toarray()
weight=tfidf.toarray()
for i in range(len(weight)):
    print("------------------\n")
    for j in range(len(word)):
        if weight[i][j] != 0:
            print(str(word[j])+"="+str(weight[i][j]),end=",")
# word=vectorizer.get_feature_names()
# #print(word)
# #aa=vectorizer.fit_transform(corpus)
# #print(aa)
# for i in range(len(word)):
#     print(i)
# for i in range(len(weight)):
#     print("------------------")
#     for j in range(len(word)):
#         if weight[i][j]!=0:
#             print(word[j],weight[i][j])
#word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
# weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
# print(tfidf)
# for i in range(len(weight)):
#     print("------------------")
#     for j in range(len(word)):
#         if weight[i][j]!=0:
#             print(word[j],weight[i][j])
# counts = [[1,1],
#           [1,0]]
# tfidf = transformer.fit_transform(counts)
# print(tfidf.toarray())