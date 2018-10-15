from sklearn.datasets import load_files
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
import jieba
import pymysql
import datetime
from sklearn.externals import joblib

categories=['电脑网络','生活服务','文化教育','娱乐休闲']
dir='C:/Users/13693/Desktop/实训/test'
four=load_files(dir,categories=categories,shuffle=True,random_state=42,encoding='utf-8',decode_error='strict')

start=datetime.datetime.time
count_vect=CountVectorizer(ngram_range=(1,1))
X_train_counts=count_vect.fit_transform(four.data)
# word=count_vect.get_feature_names()
# print(word)
# print(X_train_counts.shape[0])
# print(X_train_counts.shape[1])

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf=MultinomialNB(alpha=1e-3).fit(X_train_tfidf,four.target)


# word=['娱乐 视频']
# X_new_counts=count_vect.transform(word)
# X_new_tfidf=tfidf_transformer.transform(X_new_counts)
# predicted=clf.predict(X_new_tfidf)
# print(predicted)
# print(clf.predict_proba(X_new_tfidf))
#
# word=['学习 党校']
# X_new_counts=count_vect.transform(word)
# X_new_tfidf=tfidf_transformer.transform(X_new_counts)
# predicted=clf.predict(X_new_tfidf)
# print(predicted)
# print(clf.predict_proba(X_new_tfidf))
#
word=['培训 科技']
print(four.target_names)
X_new_counts=count_vect.transform(word)
X_new_tfidf=tfidf_transformer.transform(X_new_counts)
predicted=clf.predict(X_new_tfidf)
print(four.target_names[predicted[0]])
print(clf.predict_proba(X_new_tfidf))
#
# word=['134214234123421342134134']
# X_new_counts=count_vect.transform(word)
# X_new_tfidf=tfidf_transformer.transform(X_new_counts)
# print('X_new:',X_new_tfidf)
# predicted=clf.predict(X_new_tfidf)
# print(predicted)
# print(clf.predict_proba(X_new_tfidf)[0][0])

def JudgeCate(content):
    stopkeyword=[line.strip() for line in open(r'C:\Users\Username\Desktop\桌面整合\stopword.txt').readlines()]
    stopkeyword.extend("　")
    stopkeyword.extend(" ")
    seg=jieba.cut(content,cut_all=False)
    word=""
    for s in seg:
        if s not in stopkeyword and s.isdigit()==False:#单词不在停用词中且也不为数字
            word+=s+" "
    word=[word.strip()]
    X_new_counts=count_vect.transform(word)
    if X_new_counts.getnnz()!=0:
        X_new_tfidf=tfidf_transformer.transform(X_new_counts)
        predicted=clf.predict(X_new_tfidf)
        return four.target_names[predicted[0]][1:]#返回类别
        #print(word,four.target_names[predicted[0]])
    else:
        return '其他'

# content='娱乐'
# print(JudgeCate("淮安党校"))
#
# print(JudgeCate("淮安市生态新城福地路99号 邮编：223299"))
# print(type(cate))
# print(cate)
# 更新
# webdata_test.update({'_id': id}, {'$set':{'data': Info,'NBMtype':cate}})  # 更新到Mongodb中






