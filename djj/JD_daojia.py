import re
import requests
import json
import urllib
import time
import timeit
import math
import sys
from datetime import datetime
from dateutil import tz
import os


osenviron={}

djj_bark_cookie=''
djj_sever_jiang=''


JD_API_HOST = 'https://daojia.jd.com/client?_jdrandom='
url=''
yuanck=''
cookiesList=[]
yuanckList=[]
urlList=[]
result=''

activityId=''


zyheaders={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Content-Type": "application/x-www-form-urlencoded;","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148________appName=jdLocal&platform=iOS&djAppVersion=8.3.0&supportDJSHWK","traceparent": "00-41efefb5fc0ac1984e57912247192866-74f60f509f5e0b12-01","Referer":"https://daojia.jd.com/taroh5/h5dist/"}


djheaders={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Content-Type": "application/x-www-form-urlencoded;","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148________appName=jdLocal&platform=iOS&djAppVersion=8.3.0&supportDJSHWK","traceparent": "00-41efefb5fc0ac1984e57912247192866-74f60f509f5e0b12-01","Referer":"https://daojia.jd.com/taroh5/h5dist/"}


def JD_Daojia():
   plantBeans_getActivityInfo()
   Daojia_getUserAccountInfo()
   showSignInMsgNew()
   tasklist_Daojia()
   plantBeans_friendHelp()


def plantBeans_getActivityInfo():
   print('\n  plantBeans_getActivityInfo')
   global activityId
   try:
     body ={}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2FgetActivityInfo&isNeedDealError=true&method=POST&body='+body).text)
     activityId=data['result']['cur']['activityId']
     print(activityId)

     return data

   except Exception as e:
       print(str(e))
       
       
def showSignInMsgNew():
   print('\n showSignInMsgNew')
   try:
     body = {"platform":4,"longitude":1,"latitude":2,"source":"H5"}
     data=json.loads(iosrule('signin%2FshowSignInMsgNew',body).text)
     #print(data)
     data=data['result']['userInfoResponse']
     msg=''
     if data['hasSign']==False:
        sdata=userSigninNew()
        if sdata['msg'].find('重复')>0 or sdata['msg'].find('成功')>0:
           msg='今日已经签到,'
     else:
        msg='今日已经签到,'
     msg+=f'''已经签到{data['alreadySignInDays']}天'''
     loger(msg)
   except Exception as e:
       print(str(e))
       
def userSigninNew():
   print('\n signin_userSigninNew')
   try:
     body = {"channel":"qiandao_baibaoxiang"}
     data=json.loads(iosrule('signin%2FuserSigninNew',body).text)
     print(data['msg'])
     return data
   except Exception as e:
       print(str(e))
       
       
def Daojia_getUserAccountInfo():
   print('\n  Daojia_getUserAccountInfo')
   try:
     
     data=json.loads(requests.get(url,headers=zyheaders).text)
     #print(data)
     accountInfo=data['result']['accountInfo']['infos'][0]
     userBaseInfo=data['result']['userInfo']['userBaseInfo']
     
     msg=f'''{userBaseInfo['userName']}|{userBaseInfo['nickName']}|{userBaseInfo['mobile']}|{accountInfo[0]['accName']}{accountInfo[0]['value']}|{accountInfo[1]['accName']}{accountInfo[1]['value']}|{accountInfo[3]['accName']}{accountInfo[3]['value']}
     '''
     loger(msg)
     
   except Exception as e:
       print(str(e))
       
       
       

def tasklist_Daojia():
   print('\n tasklist_Daojia')
   try:
     body = {"modelId":"M10001","plateCode":1}
     data=json.loads(iosrule('task%2Flist',body).text)
     #print(data)
     print('到家任务列表')
     for itm in data['result']['taskInfoList']:
       m=''
       if itm['status']==3:
          m='【完成】'
       elif itm['status']==2:
          m='【领奖】'
       else:
          m='【未完成】'+str(itm['status'])
       print(f'''{itm['taskName']}={itm['taskType']}=={m}''')
     print('\n-----------------------')
     kk=0
     for itm in data['result']['taskInfoList']:
       kk+=1
       if itm['status']==3:
         print(f'''任务{len(data['result']['taskInfoList'])}-{str(kk)}: {itm['taskType']} -{itm['taskName']}-{itm['status']}已经完成✌🏻️✌🏻️✌🏻️✌🏻️''')
       if itm['status']!=3:
         print(f'''开始任务{len(data['result']['taskInfoList'])}-{str(kk)}: {itm['taskType']} -{itm['taskName']}-{itm['status']}🎁🎁🎁🎁''')
         if itm['status']==1 or itm['status']==0:
           if itm['taskType']!=506:
            task_received(itm['modelId'],itm['taskId'],itm['taskType'])
            time.sleep(2)
            task_finished(itm['modelId'],itm['taskId'],itm['taskType'])
            task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'])
            
         if itm['status']==2:
           if itm['taskType']==513:
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],1)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],2)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],3)

           else:
           	  task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'])
           time.sleep(2)
   except Exception as e:
       print(str(e))


         
         
         
def task_received(modelId,taskId,taskType):
   print('\n task_received')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     data=json.loads(iosrule('task%2Freceived',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
def task_sendPrize(modelId,taskId,taskType,subNode=1):
   print('\n task_sendPrize')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     if taskType==513:
       body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1,"subNode":subNode}
     
     data=json.loads(iosrule('task%2FsendPrize',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
       
def task_finished(modelId,taskId,taskType):
   print('\n task_finished')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":1}
     data=json.loads(iosrule('task%2Ffinished',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))


       
def plantBeans_friendHelp():
   print('\n  plantBeans_friendHelp')
   try:
     body ={"activityId":"23b972077009e05","groupId":"100006608792191"}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrule('xapp%2FfriendHelp%2Fdetail&isNeedDealError=true&method=POST&body='+body).text)
     print(data)

    
   except Exception as e:
       print(str(e))
       
       


       
def iosrule(functionId,body={}):
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   
   timeArray = time.strptime(Localtime, "%Y-%m-%d %H:%M:%S")
   timeStamp = int(time.mktime(timeArray))
   url=JD_API_HOST+f'''{timeStamp}&functionId={functionId}&isNeedDealError=true&body={urllib.parse.quote(json.dumps(body))}&channel=ios&platform=6.6.0&platCode=h5&appVersion=6.6.0&appName=paidaojia&deviceModel=appmodel'''

   try:
      response=requests.get(url,headers=djheaders)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))


def iosrulex(body):
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   
   timeArray = time.strptime(Localtime, "%Y-%m-%d %H:%M:%S")
   timeStamp = int(time.mktime(timeArray))
   url=JD_API_HOST+str(timeStamp)
   try:
      response=requests.post(url,headers=djheaders,data=body)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))
def TotalBean(cookies,checkck):
   print('检验过期')
   signmd5=False
   headers= {
        "Cookie": cookies,
        "Referer": 'https://home.m.jd.com/myJd/newhome.action?',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
      }
   try:
       ckresult= requests.get('https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New',headers=headers,timeout=10).json()
       #print(ckresult)
       if ckresult['retcode']==0:
           signmd5=True
           loger(f'''【京东{checkck}】''')
       else:
       	  signmd5=False
       	  msg=f'''【京东账号{checkck}】cookie已失效,请重新登录京东获取'''
       	  print(msg)
          pushmsg(msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5

def check(flag,list):
   vip=''
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if flag in os.environ:
      vip = os.environ[flag]
   if flag in osenviron:
      vip = osenviron[flag]
   if vip:
       for line in vip.split('\n'):
         if not line:
            continue 
         list.append(line.strip())
       return list
   else:
       print(f'''【{flag}】 is empty,DTask is over.''')
       exit()

def pushmsg(title,txt,bflag=1,wflag=1):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   if bflag==1 and djj_bark_cookie.strip():
      print("\n【通知汇总】")
      purl = f'''https://api.day.app/{djj_bark_cookie}/{title}/{txt}'''
      response = requests.post(purl)
      #print(response.text)
   if wflag==1 and djj_sever_jiang.strip():
      print("\n【微信消息】")
      purl = f'''http://sc.ftqq.com/{djj_sever_jiang}.send'''
      headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
      body=f'''text={txt})&desp={title}'''
      response = requests.post(purl,headers=headers,data=body)
   global result
   print(result)
   result =''
    
def loger(m):
   #print(m)
   global result
   result +=m
    
def islogon(j,count):
    JD_islogn=False
    global jd_name
    for i in count.split(';'):
       if i.find('pin=')>=0:
          jd_name=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(j)}开始】{jd_name}''')
    if(TotalBean(count,jd_name)):
        JD_islogn=True
    return JD_islogn
   
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def start():
   
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", )
   
   timeArray = time.strptime(Localtime, "%Y-%m-%d %H:%M:%S")
   timeStamp = int(time.mktime(timeArray))
   print('Localtime',Localtime)
   
   global djheaders,zyheaders,url,yuanck
   check('DJJ_DAOJIA_COOKIE',cookiesList)
   check('DJJ_DAOJIA_URL',urlList)
   check('DJJ_YUAN_CK',yuanckList)
   j=0
   for count in cookiesList:
        j+=1
        djheaders['Cookie']=count
        url=urlList[j-1]
        yuanck=yuanckList[j-1]
        zyheaders['Cookie']=yuanck
        JD_Daojia()
     #time.sleep(30)
   pushmsg('JD_DaoJia',result)
   
if __name__ == '__main__':
       start()
