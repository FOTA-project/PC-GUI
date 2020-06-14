import pyrebase
from pathlib import Path
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QThread, QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2 import QtCore ,QtWidgets

import sys , time , threading

import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

from ctypes import windll

#import progress_script
#import upload_script



file_path = ''

INSTRUCTION_WRITE_MAX_REQUESTS    = -4
INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

STOP_THREAD_FLAG=0

# upload
firebaseConfig = {
    "apiKey": "AIzaSyBgBFhNa6OnJCLbFTQW3vF_Cyz-rMyN4vU",
    "authDomain": "fota-server-b4148.firebaseapp.com",
    "databaseURL": "https://fota-server-b4148.firebaseio.com",
    "projectId": "fota-server-b4148",
    "storageBucket": "fota-server-b4148.appspot.com",
    "messagingSenderId": "774423425890",
    "appId": "1:774423425890:web:f506832444c3d30b2c323b",
    "measurementId": "G-2DE9D9TN6N"
  };

# admin credentials
email = r"admin_stm32@admin-group.com"
password = r"123lolxd"

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig);
auth = firebase.auth()
admin = auth.sign_in_with_email_and_password(email, password)
admin = auth.refresh(admin['refreshToken']) # optional

db = firebase.database()
storage = firebase.storage()

#admin_uid = admin['userId']
admin_tokenId = admin['idToken']

user_db_dir = ''

users = db.child("users").get(admin_tokenId)
userNameUID = {}

for uid, userInfo in users.val().items():
    userNameUID[userInfo['Name']] = uid

maxRequests = -1

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(552, 301)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75);
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Browse_pushButton = QPushButton(self.centralwidget)
        self.Browse_pushButton.setObjectName(u"Browse_pushButton")
        self.Browse_pushButton.setGeometry(QRect(420, 120, 112, 41))
        self.Browse_pushButton.setFont(font)
        self.Browse_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.Upload_pushButton = QPushButton(self.centralwidget)
        self.Upload_pushButton.setObjectName(u"Upload_pushButton")
        self.Upload_pushButton.setGeometry(QRect(420, 190, 112, 41))
        self.Upload_pushButton.setFont(font)
        self.Upload_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.comboBox = QComboBox(self.centralwidget)
        
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(420, 60, 111, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox.setFont(font1)
        self.comboBox.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(410, 20, 111, 20))
        self.label.setFont(font)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 391, 221))
        self.frame.setStyleSheet(u"image: url(icon.png);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(18, 239, 81, 31))
        self.label_2.setFont(font)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(260, 240, 291, 31))
        #self.progressBar.setValue(24)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(105, 240, 140, 31))
        self.lineEdit.setFont(font1)
        self.lineEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        ## we edit here 
        self.Upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)
        self.setIcon(MainWindow)
        self.worker = Worker()
    # setupUi

    def setIcon(self,MainWindow):
        appIcon = QIcon("icon.png")
        MainWindow.setWindowIcon(appIcon)
    
    def Browse_Handler(self):
      global file_path
      root = tk.Tk()
      root.withdraw()
      #root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetype= ([("Elf files","*.elf")]))
      file_path = root.filepath

  
    def setProgress(self, progress, max):
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(progress)
        
        if progress >= max: #if finished
            # update isNewElf flag in database
            db.child(user_db_dir).update({"elfProgress" : 0}, admin_tokenId)
            
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Flash done", None))
            self.worker.stop()
        elif progress == -1: #if timed out
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Flash error", None))
            self.worker.stop()


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FOTA PC-GUI", None))
        self.Browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.Upload_pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        
        i = 0
        for userName in userNameUID:
            self.comboBox.setItemText(i, QCoreApplication.translate("MainWindow", userName, None))
            i = i + 1

        self.label.setText(QCoreApplication.translate("MainWindow", u"    USERS", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"  Status", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"        Idle", None))
        
        ElfProgress = db.child(user_db_dir + "/elfProgress").get(admin_tokenId).val()
        userChoice=0
        if ElfProgress != 0:
            userChoice=ctypes.windll.user32.MessageBoxW(0, "Do you want to resume ?", "Error in previous flashing process", 4)
            #Yes response
            if userChoice==6:
                db.child(user_db_dir).update({"isNewElf" : 1}, admin_tokenId)
                self.worker.updateProgress.connect(self.setProgress)
                self.worker.start()
            
            elif userChoice==7:
                db.child(user_db_dir).update({"elfProgress" : 0}, admin_tokenId)

        
        
    # retranslateUi
    
    def UploadElfFile(self, file_path, user_uid):
        global admin_tokenId
        global user_db_dir
        
        local_file = file_path
        cloud_file = "users/" + user_uid + "/file.elf"
        user_db_dir = "users/" + user_uid + "/STM32"

        # upload file
        storage.child(cloud_file).put(local_file, admin_tokenId)

        # update isNewElf flag in database
        db.child(user_db_dir).update({"elfProgressMaxRequest" : -1}, admin_tokenId)
        db.child(user_db_dir).update({"isNewElf" : 1}, admin_tokenId)
        
        isNewElf = db.child(user_db_dir + "/isNewElf").get(admin_tokenId).val()
        
        return (isNewElf ^ 1) #return state if uploud done or not 
        

    def Upload_Handler(self):
        global user
        global state
        global maxRequests
        global user_db_dir
        global admin_tokenId
        
        user = userNameUID[self.comboBox.currentText()]
        
        self.progressBar.setMaximum(100)
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Uploading..", None))
        self.progressBar.reset()
        self.progressBar.setValue(50)
            
        state = self.UploadElfFile(file_path, user)

        if state == 1: #There is an error
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Error.. ", None))
            return
            #TODO: Add message to complete or cancelling in case of errors
            #value=ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)
        
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Upload done", None))
        #TODO : edit progress to move from 0 to 100
        self.progressBar.setValue(100)
        time.sleep(1)

        timeoutCtr = 0
        isTerminate = 0
        previousElfProgress = -1

        # get max number of requests from server
        while 1:
            time.sleep(0.1) # 100ms
            maxRequests = db.child(user_db_dir + "/elfProgressMaxRequest").get(admin_tokenId).val()
            if maxRequests != -1:
                timeoutCtr = 0
                break
            else: # if RPi communicator didn't update value
                timeoutCtr = timeoutCtr + 1
                
            if timeoutCtr == 10: #1sec, if timed out
                isTerminate = 1 # set the flag to skip next loop
                self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Flash not responding", None))
                self.progressBar.reset()
                break

        if isTerminate == 0: # if no error occured
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Flashing.....", None))
            self.progressBar.reset()
            self.worker.updateProgress.connect(self.setProgress)
            self.worker.start()
        



class Worker(QtCore.QThread):
    updateProgress = QtCore.Signal(int, int)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        global maxRequests
        global user_db_dir
        global admin_tokenId
        
        ElfProgress = 0
        
        timeoutCtr = 0
        isTerminate = 0
        previousElfProgress = -1
        
        while 1:
            ElfProgress = db.child(user_db_dir + "/elfProgress").get(admin_tokenId).val()
            
            if ElfProgress != previousElfProgress:
                timeoutCtr = 0
                previousElfProgress = ElfProgress
                self.updateProgress.emit(int(ElfProgress), int(maxRequests))
            else: # if no change happened
                time.sleep(0.1) # 100ms
                timeoutCtr = timeoutCtr + 1

            if timeoutCtr == 5: #500ms, if timed out
                self.updateProgress.emit(int(-1), int(maxRequests))


    def stop(self):
        print()
        self.requestInterruption()
        self.terminate()
        
        

app = QApplication(sys.argv)
window = QMainWindow()
Form = Ui_MainWindow()
Form.setupUi(window)
window.show()
sys.exit(app.exec_())

