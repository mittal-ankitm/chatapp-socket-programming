from PyQt5 import uic,QtWidgets,QtCore
from pymongo import MongoClient
loginbool=True
import key
loginui=uic.loadUi("ui/login.ui")
client=MongoClient(key.url)
db=client.chatapp
users=db.users
import search
def validate_id():
    userid=loginui.userid.text()
    pwd=loginui.pwd.text()
    err=loginui.err
    err.hide()
    s=True
    if len(userid)==0:
        err.setText("enter userid")
        err.show()
        s= False
        return False
    if len(pwd)==0:
        err.setText("enter password")
        err.show()
        s = False
        return False
    r=users.find_one({"userid":userid})
    if not r:
        print(r)
        err.setText("no account found.")
        err.show()
        s=False
        return False
    else:
        
        if pwd!=r['password']:
            err.setText("password incorrect.")
            err.show()
            s=False
            return False
        if s:
            userid=r['userid']
            
            loginui.close()
            search.search(userid)
            



def login():
    loginui.userid.setText("")
    loginui.userid.setPlaceholderText("User id")

    loginui.pwd.setPlaceholderText("Password")
    loginui.userid.setAlignment(QtCore.Qt.AlignCenter)
    loginui.pwd.setAlignment(QtCore.Qt.AlignCenter)
    loginui.pwd.setText("")

    loginui.pwd.setEchoMode(QtWidgets.QLineEdit.Password)

    err = loginui.err
    err.hide()

    global loginbool
    if loginbool:
        loginui.logbutton.clicked.connect(validate_id)
        loginbool=False
    loginui.show()
