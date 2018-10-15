#encoding: utf-8
import pymongo
import charts
client=pymongo.MongoClient("localhost",27017)
webtest=client["jerry"]
webdata=webtest["test2"]


def someonestudent():
    pipeline=[
        {'$match':{'NBMtype':{'$exists':True}}},
        {'$group':{'_id':{'user':'$user_crc','type':'$NBMtype'},'counts': {'$sum': 1}}},
        {'$sort':{'counts':-1}},
    ]
    for info in webdata.aggregate(pipeline):
        yield info

user=set()
cate=[]
education=0
service=0
computer=0
entertainment=0
other=0
for i in someonestudent():
    if i['_id']['user'] not in user:
        user.add(i['_id']['user'])
        if i['_id']['type']=="文化教育":
            education+=1
        elif i['_id']['type']=="生活服务":
            service+=1
        elif i['_id']['type'] == "电脑网络":
            computer+=1
        elif i['_id']['type'] == "娱乐休闲":
            entertainment+=1
        else:
            other+=1

nbm_options={
    'chart':    {'zoomType':'xy'},
    'title':    {'text':'2015-12-26淮阴工学院学生整体网页浏览分布'},
    'tooltip': {
        'headerFormat': '{series.name}<br>',
        'pointFormat': '{point.name}: <b>{point.percentage:.1f}%</b>'
    },
    'plotOptions': {
            'pie': {
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
                }
            }
        },
}
nbm_series=[
    {
        'type':'pie',
        'name':'pie chart',
        'data':[["文化教育",education],["生活服务",service],["电脑网络",computer],["娱乐休闲",entertainment],["其他",other]]
    }
]
charts.plot(nbm_series,options=nbm_options)
