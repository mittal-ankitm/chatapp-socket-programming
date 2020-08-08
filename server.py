import socket
import threading
import sys
import datetime
import key
from pymongo import MongoClient
client=MongoClient(key.url)
db=client.chatapp
users=db.users
messages=db.messages

connections={}


def handler(c,a,userid):
     while True:

        data=c.recv(1024)
        dt=str(data,'utf-8').split(",")
        userid2=dt[0]
        msg=dt[1]
        messages.insert_one({'from':userid,'to':userid2,'msg':msg,'time': str(datetime.datetime.now())})
        senddata=str(userid)+","+msg
        if(userid2 in connections):
            connections[userid2][0].send(bytes(senddata,'utf-8'))

        if not data:
            print(str(a[0])+":"+str(a[1]) ,"disconnected")
            del connections[userid]
            c.close()
            break


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('',5000))
sock.listen(5)

while True:
    c,a=sock.accept()
    userid=str(c.recv(1024),'utf-8')
    cthread=threading.Thread(target=handler,args=(c,a,userid))
    cthread.daemon=True
    cthread.start()
    connections[userid]=[c,a]
    print(str(a[0])+":"+str(a[1]) ,"connected")

    



