#!/bin/python
import requests 
import sys
import os
import threading
import urllib3

class MyThread(threading.Thread):
    def __init__(self, st,to):
        threading.Thread.__init__(self)
        self.st = st
        self.to = to
    def run(self):
        syncUser(self.st,self.to)

def syncUser(st,to):
    file=os.open('user'+str(st)+'-'+str(to)+'.csv', os.O_RDWR|os.O_CREAT)
    uid=st
    s = requests.session()
    while uid < to:
        print(uid,file=sys.stderr)
        req = requests.Request('GET','https://mshopapi.hengan.cn/mall/test/nascent/addBatchUser?fromUid='+str(uid)+'&toUid='+str(uid+100))
        prep = s.prepare_request(req)
        r = s.send(prep,stream=False)
        os.write(file,bytes(r.text,encoding="utf-8"))
        os.write(file,bytes("\n",encoding="utf-8"))
        uid = uid + 100
    s.close()
    print('done',file=sys.stderr)
    os.close(file)
threads = []
i=0;
uid=0
while uid < 233300:
    st=uid
    ed=uid+50000
    if ed > 233300:
                ed = 233300
    threads.append(MyThread(st,ed))
    threads[i].start()
    i = i+1
    uid = ed
for th in threads:
    th.join()

