from PyQt5 import uic,QtWidgets,QtCore
from pymongo import MongoClient
searchbool=True
import key
searchui=uic.loadUi("ui/search.ui")

client=MongoClient(key.url)
db=client.chatapp
users=db.users
import chatbox
userid=0
usertoid=0

def searchfunc():
    query=searchui.query.text()
    err=searchui.err
    res=users.find_one({'userid':query})
    if not res:
        err.setText("no user found")
        err.show()
    else:
        usertoid=query
        searchui.close()
        chatbox.chatbox(userid,usertoid)
        


def search(user_id):
    global userid
    global usertoid
    userid=user_id
    searchui.query.setText("")
    searchui.query.setPlaceholderText("search")

    searchui.query.setAlignment(QtCore.Qt.AlignCenter)

    err = searchui.err
    err.hide()

    global searchbool
    if searchbool:
        searchui.searchbutton.clicked.connect(searchfunc)
        searchbool=False
    searchui.show()
