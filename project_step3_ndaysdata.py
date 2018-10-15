import pymongo
client=pymongo.MongoClient('localhost',27017)
student=client['webtest']
allstudent=student['allstudent']
r201=''
def init(date):
    global r201
    r201=student[date]
    print(date)
def Pipe_data(user):
    pipe=[
        {'$match':{'$and':[{'data':{'$exists':True}},{'data':{'$nin':['None']}},{'user_crc':user}]}},
        {'$group':{'_id':{'type':'$NBMtype','user':'$user_crc'},'counts':{'$sum':1}}}
    ]
    return pipe
#print(counts)
#user1:3910202730
#user2:68573644
#user3:2636056694
def InsertToMongo(user,type,counts,percent,date):
    allstudent.insert({'user':user,'type':type,'counts':counts,'percent':percent,'date':date})  # 更新到Mongodb中
def UpdateNewTableStudent(user,date):
    pipe=Pipe_data(user)
    sumpage = r201.find(
        {'$and': [{'data': {'$exists': True}}, {'data': {'$nin': ['None']}}, {'user_crc': user}]}).count()
    flag1=0
    flag2=0
    flag3=0
    flag4=0
    for info in r201.aggregate(pipe):
        user=info['_id']['user']
        type=info['_id']['type']
        counts=info['counts']
        percent=round(info['counts']/sumpage*100)
        print(user,type,counts,percent,date)
        InsertToMongo(user,type,counts,percent,date)
        if type=='生活服务':
            flag1=1
        if type=='电脑网络':
            flag2=1
        if type=='娱乐休闲':
            flag3=1
        if type=='文化教育':
            flag4=1
    if flag1==0:
        print(user,'生活服务',0,0,date)
        InsertToMongo(user,'生活服务',0,0,date)
    if flag2==0:
        print(user,'电脑网络',0,0,date)
        InsertToMongo(user,'电脑网络',0,0,date)
    if flag3==0:
        print(user,'娱乐休闲',0,0,date)
        InsertToMongo(user,'娱乐休闲',0,0,date)
    if flag4==0:
        print(user,'文化教育',0,0,date)
        InsertToMongo(user,'文化教育',0,0,date)

def CurrentUser(date):
    user_list=['2684111136','2574133163','240563119','1870978388']
    for u in user_list:
        UpdateNewTableStudent(u,date)

date_list=['r20151226','r20151227','r20151228','r20151229','r20151230','r20151231','r20160101','r20160102','r20160103','r20160104','r20160105','r20160106','r20160107','r20160111','r20160112','r20160113','r20160114','r20160115','r20160116']
for date in date_list:
    init(date)
    print(date[1:])
    CurrentUser(date[1:])



