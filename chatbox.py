from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import socket
import threading
import sys
import key
chatboxbool=True
chatboxui=uic.loadUi("ui/chatbox.ui")
userid=0
usertoid=0
from pymongo import MongoClient
client=MongoClient(key.url)
db=client.chatapp
users=db.users
messages=db.messages
sock=0
import search

def getmsg(signobject):
    global sock
    
    while True:
        data=sock.recv(1024)
        msg=str(data,'utf-8').split(',')
        if not data:
            break
        if(msg[0]==usertoid):
            signobject.emitsign(msg[1])        
        
class signobj(QObject):
    sign=pyqtSignal(str)

    def emitsign(self,str):
        self.sign.emit(str)

def timestamp(arr):
    return arr[2]

def loaddata():
    arr=[]
    for message in messages.find({'from':userid,'to':usertoid}):
        arr.append([1,message['msg'],message['time']])
    for message in messages.find({'from':usertoid,'to':userid}):
        arr.append([2,message['msg'],message['time']])
    arr.sort(key=timestamp)
    for el in arr:
        if(el[0]==1):
            chatboxui.msgbox.addWidget(QLabel("you : "+el[1]))
        else:
            chatboxui.msgbox.addWidget(QLabel(usertoid+" : "+el[1]))

    


def sendmsg():
    global sock
    msg=chatboxui.msg.text()
    data=usertoid+","+msg
    sock.send(bytes(data,'utf-8'))
    chatboxui.msgbox.addWidget(QLabel("you : "+msg))

@pyqtSlot(str)
def on_sign(msgstring):
    chatboxui.msgbox.addWidget(QLabel(usertoid+" : "+msgstring))

def searchpage():
    chatboxui.close()
    search.search(userid)

def chatbox(userid_id,userto_id):
    global sock
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',5000))
    global userid,usertoid
    
    userid=userid_id
    usertoid=userto_id
    loaddata()
    sock.send(bytes(userid,'utf-8'))
    signobject=signobj()
    signobject.sign.connect(on_sign)
    ithread=threading.Thread(target=getmsg,args=(signobject,))
    ithread.daemon=True
    ithread.start()

    chatboxui.username.setText(usertoid)

  


    global chatboxbool
    if chatboxbool:
        chatboxui.sendbutton.clicked.connect(sendmsg)
        chatboxui.backbutton.clicked.connect(searchpage)
        chatboxbool=False
    chatboxui.show()

