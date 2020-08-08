from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from pymongo import MongoClient
import key
client=MongoClient(key.url)
import re
import login
import search
registerbool=True
regui=uic.loadUi("ui/reg.ui")
db=client.chatapp
users=db.users
def check_email(email):
    if len(email) > 7:
        if re.match("^[a-zA-Z][a-zA-Z0-9._]+@[a-zA-Z]{2,8}[.]+[a-zA-Z.]{2,7}$", email)!=None:
            return True
    return False


def validate_reg():
    s=True
    email = regui.email.text()
    userid = regui.userid.text()
    pwd = regui.pwd.text()
    err=regui.errorbar

    if check_email(email)==False:
        err.setText("enter valid email")
        err.show()
        s=False
    if len(userid)<7:
        err.setText("userid should be more than 7 character")
        err.show()
        s=False
    if len(pwd)<8:
        err.setText("password should be more than 8 character")
        err.show()
        s=False

    
    
    if users.find_one({'userid':userid}):
        err.setText("userid not availaible")
        err.show()
        s=False
    if users.find_one({'email':email}):
        err.setText("email already registered")
        err.show()
        s=False

    if s:
        users.insert_one({'userid':userid,'email':email,'password':pwd})
        regui.close()
        search.search(userid)

def loginpage():
    regui.close()
    login.login()


def reg():
    regui.userid.setText("")
    regui.email.setText("")
    regui.pwd.setText("")

    regui.userid.setPlaceholderText("User id")
    regui.userid.setAlignment(QtCore.Qt.AlignCenter)
    regui.userid.setMaxLength(30)
    regui.email.setPlaceholderText("Email")
    regui.email.setAlignment(QtCore.Qt.AlignCenter)
    regui.email.setMaxLength(30)
    regui.pwd.setPlaceholderText("Password")
    regui.pwd.setAlignment(QtCore.Qt.AlignCenter)
    regui.pwd.setMaxLength(30)
  

    err = regui.errorbar
    err.hide()

    regui.pwd.setEchoMode(QtWidgets.QLineEdit.Password)

    global registerbool
    if registerbool:
        regui.regbutton.clicked.connect(validate_reg)
        regui.logbutton.clicked.connect(loginpage)
        registerbool=False

    regui.show()



