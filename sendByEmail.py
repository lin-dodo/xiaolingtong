# -*- coding: utf-8 -*-
import urllib,json
from time import sleep
from sms import *
while 1:
    u=urllib.urlopen("http://umlxiaolingtong.sinaapp.com/searchtask/?type=email")
    con=u.read()
    data=json.loads(con)
    if data['errCode']==0:
        ll=data['data']
        for i in ll:
            t=i['task']
            send_list=i['target']
            for i in send_list.split(","):
                print i
                send_mail(t,i)
    else:
        print "无要发送的通知!"
    sleep(1800)
        
        
    
