#encoding: utf-8
import pymongo
import charts

import matplotlib.pyplot as plt
client=pymongo.MongoClient("localhost",27017)
webtest=client["jerry"]
webdata_test=webtest["test2"]
def nbmdata():
    pipeline=[
        {'$match':{'$and':[{'SVMtype':{'$exists':True}},{'SVMtype':{"$in":['文化教育','生活服务','娱乐休闲','电脑网络','其他']}}]}},
        {'$group':{'_id':'$NBMtype','counts':{'$sum':1}}},
        {'$sort':{'counts':-1}}
    ]
    for i in webdata_test.aggregate(pipeline):
        yield i['_id'],i['counts']

nbm_series=[
    {
        'type':'pie',
        'name':'pie chart',
        'data':[i for i in nbmdata()]
    }
]
nbm_options={
    'chart':    {'zoomType':'xy'},
    'title':    {'text':'NBM后URL类别统计'},
    #'subtitle': {'text':'4月1日的二手物品的发帖量'},
    #'xAxis':    {'categories':[if 'Arm':'体育']},
    #'yAxis':    {'title':{'text':'数量'}}
}
#显示分类比例
#charts.plot(nbm_series,options=nbm_options)
charts.plot(nbm_series,options=nbm_options)

#显示Top10
# def top10():
#     pipeline=[
#         {'$match':{'data.url':{'$nin':[None]}}},
#         {'$group':{'_id':'$data.url','counts':{'$sum':1}}},
#         {'$sort':{'counts':-1}},
#         {"$limit":10}
#     ]
#     for i in webdata_test.aggregate(pipeline):
#         yield i['_id'],i['counts']
# for i in top10():
#     print(i)
# def userTop10():
#     pipeline = [
#             {'$group':{'_id':'$user_crc','counts':{'$sum':1}}},
#             {'$sort':{'counts':-1}},
#             {"$limit":10}
#         ]
#     for i in webdata_test.aggregate(pipeline):
#         yield i['_id'],i['counts']
# for i in userTop10():
#     print(i)
#2608266266  179877
#1083244360 114259

def xxusertop10():
    pipeline=[
        {'$match':{'user_crc':'1083244360'}},
        {'$group':{'_id':'$result.url','counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {"$limit":10}
    ]
    for i in webdata_test.aggregate(pipeline):
        yield i['_id'],i['counts']
for i in xxusertop10():
    print(i)