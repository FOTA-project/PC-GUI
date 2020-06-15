import pyrebase
from pathlib import Path
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint, QThread, QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2 import QtCore ,QtWidgets

import sys , time , threading,os

import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

from ctypes import windll


STOP_THREAD_FLAG = 0

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

currentUserUID = '' # currently selected user UID from combobox

admin_tokenId = admin['idToken']

user_db_dir = ''

users = db.child("users").get(admin_tokenId)
userNameUID = {}

# am empty user to solve combobox selection issue
userNameUID[''] = ''

for uid, userInfo in users.val().items():
    userNameUID[userInfo['Name']] = uid

file_path = ''

INSTRUCTION_WRITE_MAX_REQUESTS    = -4
INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

isTokenRefreshThreadActive = 0
isUserAlive = 0

isUploadProcessHappening = 0

def Admin_TokenRefresh_Thread():
    global admin
    global isTokenRefreshThreadActive
    
    while 1:
        isTokenRefreshThreadActive = 1
        admin = auth.refresh(admin['refreshToken']) # get a new token
        isTokenRefreshThreadActive = 0
        time.sleep(1800) # sleep 30min

# admin token refresher
tokenThreadHandle = threading.Thread(target = Admin_TokenRefresh_Thread)
#tokenThreadHandle.start()

time.sleep(1)


class Ui_MainWindow(object):
    def closeEvent(self, event):
        print("ASssssssdasdasdsadsadasdasd#########################")
        event.accept()


    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        
        # set a fixed size for the main window
        width = 550
        height = 335
        #MainWindow.resize(width, height)
        MainWindow.setFixedSize(width, height) 
        
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
        self.label_2.setGeometry(QRect(10, 240, 81, 31))
        self.label_2.setFont(font)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(260, 240, 291, 31))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(105, 240, 140, 31))
        self.lineEdit.setFont(font1)
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(150, 280, 321, 31))
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)
        self.label_3= QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 280, 131, 31))
        self.label_3.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        ## we edit here 
        self.Upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)

        # when an item in the combobox is clicked
        self.comboBox.textActivated.connect(self.on_combobox_changed)

        self.setIcon(MainWindow)

        # connect progress bar thread
        self.flashingProgressAttribute = FlashingProgressThread()
        self.flashingProgressAttribute.updateProgress.connect(self.setProgress)
        self.flashingProgressAttribute.statusBarSignal.connect(self.setStatusBarState)
        self.flashingProgressAttribute.exitSignal.connect(self.flashStateReceiver)

        # connect user life checking thread
        self.userLifeAttributes = UserLifeRefresher()
        self.userLifeAttributes.uploadBtnEnableSignal.connect(self.setUploadBtnState)
        self.userLifeAttributes.browseBtnEnableSignal.connect(self.setBrowseBtnState)
        self.userLifeAttributes.statusBarSignal.connect(self.setStatusBarState)

        # connect uploader thread
        self.uploadStateAttribute = UploaderThread()
        self.uploadStateAttribute.uploadStateSignal.connect(self.uploadStateReceiver)
        self.uploadStateAttribute.statusBarSignal.connect(self.setStatusBarState)
        self.uploadStateAttribute.progressBarSignal.connect(self.setProgress)

        # initially disable upload and browse buttons
        self.Upload_pushButton.setEnabled(False)
        self.Browse_pushButton.setEnabled(False)

    # setupUi


    def uploadStateReceiver(self, state):
        global isUploadProcessHappening

        self.uploadStateAttribute.stop()

        if state == False: #There is an error
            # hint to the life checker thread
            isUploadProcessHappening = 0

            # enable upload button
            self.Upload_pushButton.setEnabled(True)

            # enable browse button
            self.Browse_pushButton.setEnabled(True)

            # enable browse button
            self.comboBox.setEnabled(True)

            return

        # start the flashing progress thread
        self.flashingProgressAttribute.start()


    def flashStateReceiver(self):
        global isUploadProcessHappening

        # hint to the life checker thread
        isUploadProcessHappening = 0

        self.flashingProgressAttribute.stop()

        # enable upload button
        self.Upload_pushButton.setEnabled(True)

        # enable browse button
        self.Browse_pushButton.setEnabled(True)

        # enable browse button
        self.comboBox.setEnabled(True)


    def setUploadBtnState(self, state):
        self.Upload_pushButton.setEnabled(state)


    def setBrowseBtnState(self, state):
        self.Browse_pushButton.setEnabled(state)


    def setStatusBarState(self, colors, displayText):
        self.lineEdit.setStyleSheet(colors)
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", displayText, None))


    def setProgress(self, progress, max):
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(progress)


    def setIcon(self,MainWindow):
        appIcon = QIcon("icon.png")
        MainWindow.setWindowIcon(appIcon)


    def Browse_Handler(self):
      global file_path
      
      root = tk.Tk()
      root.withdraw()
      #root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetype= ([("Elf files","*.elf")]))
      
      if root.filepath != '': # if any file is selected (user didn't press cancel)
        file_path = root.filepath
      
      if file_path != '': # if this variable holds anything (initialized with any filepath)
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", os.path.basename(file_path), None))
      else: # if user pressed cancel (didn't select file)
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"There is no chosen ELF file ", None))

  
    def retranslateUi(self, MainWindow):
        global userNameUID
        
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FOTA PC-GUI", None))
        self.Browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.Upload_pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        
        i = 0
        for userName in userNameUID:
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, QCoreApplication.translate("MainWindow", userName, None))
            i = i + 1

        self.label.setText(QCoreApplication.translate("MainWindow", u"      Users list", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"  Status", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"  Current file", None))
        self.lineEdit.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Idle", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"There is no chosen ELF file ", None))
        
    # retranslateUi
    

    def Upload_Handler(self):
        global state
        global user_db_dir
        global admin_tokenId
        global userNameUID
        global file_path
        global currentUserUID
        global isUploadProcessHappening
        
        if file_path == '':
            self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"Select an ELF file before uploading", None))
            return
        
        if currentUserUID == '': # 1st empty/dummy user       
            self.lineEdit.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(100, 0, 0);")
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"No user selected", None))
            return

        # disable upload button
        self.Upload_pushButton.setEnabled(False)

        # disable browse button
        self.Browse_pushButton.setEnabled(False)

        # disable browse button
        self.comboBox.setEnabled(False)

        # raise the global flag to hint to the life checker thread
        isUploadProcessHappening = 1

        # start upload thread
        self.uploadStateAttribute.start()

  
    def on_combobox_changed(self, value):
        global user_db_dir
        global isTokenRefreshThreadActive
        global admin_tokenId
        global currentUserUID
        global userNameUID
        
        # stop life check thread
        if self.userLifeAttributes.isRunning() == True:
            self.userLifeAttributes.stop()
        
        # initially disable upload and browse buttons until user life thread checks
        self.Upload_pushButton.setEnabled(False)
        self.Browse_pushButton.setEnabled(False)

        # initially reset progress bar
        self.progressBar.reset()

        if value == '': # 1st empty/dummy user        
            self.lineEdit.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Idle", None))
            return
        
        # print idle on the status bar
        self.lineEdit.setStyleSheet("color: rgb(0, 0, 0); background-color: rgb(255, 255, 0);")
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Checking RPi...", None))

        # trap until admin token refresh thread is over/done
        while isTokenRefreshThreadActive == 1:
            time.sleep(0.05) # wait 50ms
        
        self.userLifeAttributes.start() # start life check thread

        user_uid = userNameUID[value]
        currentUserUID = user_uid # update the global flag
        user_db_dir = "users/" + user_uid + "/STM32"
        
        ElfProgress = db.child(user_db_dir + "/elfProgress").get(admin_tokenId).val()
        userChoice = 0
        if ElfProgress != 0:
            userChoice = windll.user32.MessageBoxW(0, "Do you want to resume ?", "Error in previous flashing process", 4)
            if userChoice == 6: # resume
                db.child(user_db_dir).update({"isNewElf" : 1}, admin_tokenId)
                self.flashingProgressAttribute.start()
            elif userChoice == 7: # reset
                db.child(user_db_dir).update({"elfProgress" : 0}, admin_tokenId)


# flashing progress thread
class FlashingProgressThread(QtCore.QThread):
    updateProgress = QtCore.Signal(int, int)
    statusBarSignal = QtCore.Signal(str, str)
    exitSignal = QtCore.Signal()
    
    def __init__(self):
        QtCore.QThread.__init__(self)


    def run(self):
        global user_db_dir
        global admin_tokenId

        timeoutCtr = 0
        isTerminate = 0
        ElfProgress = 0
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
                
            if timeoutCtr == 20: #2sec, if timed out
                isTerminate = 1 # set the flag to skip next loop
                self.statusBarSignal.emit("color: rgb(255, 255, 255); background-color: rgb(100, 0, 0);", u"RPi not responding")
                self.updateProgress.emit(0, 100)
                break

        if isTerminate == 0: # if no error occurred when getting max requests from server
            self.updateProgress.emit(0, maxRequests)
            self.statusBarSignal.emit("color: rgb(0, 0, 0); background-color: rgb(255, 255, 0);", u" Flashing...")

        # we get here if we received max requests from server

        while isTerminate == 0:
            ElfProgress = db.child(user_db_dir + "/elfProgress").get(admin_tokenId).val()

            if ElfProgress != previousElfProgress: # if a change happened in the database of the user
                timeoutCtr = 0
                previousElfProgress = ElfProgress
                self.updateProgress.emit(ElfProgress, maxRequests)
                
                if ElfProgress >= maxRequests: #if finished
                    # update isNewElf flag in database
                    db.child(user_db_dir).update({"elfProgress" : 0}, admin_tokenId)
                    
                    self.statusBarSignal.emit("color: rgb(0, 0, 0); background-color: rgb(0, 255, 0);", u"Flash done")
                    
                    isTerminate = 1
            else: # if no change happened
                time.sleep(0.1) # 100ms
                timeoutCtr = timeoutCtr + 1

            if timeoutCtr == 15: #1500ms, if timed out
                self.updateProgress.emit(0, maxRequests)
                self.statusBarSignal.emit("color: rgb(255, 255, 255); background-color: rgb(100, 0, 0);", u"Flash error")
                
                isTerminate = 1

        self.exitSignal.emit()


    def stop(self):
        self.requestInterruption()
        self.terminate()


class UserLifeRefresher(QtCore.QThread):
    uploadBtnEnableSignal = QtCore.Signal(bool)
    browseBtnEnableSignal = QtCore.Signal(bool)
    statusBarSignal = QtCore.Signal(str, str)
    
    def __init__(self):
        QtCore.QThread.__init__(self)


    def run(self):
        global admin
        global currentUserUID
        global admin_tokenId
        global isTokenRefreshThreadActive
        global isUserAlive
        global isUploadProcessHappening
        
        errorCtr = 0
        isFirstTime = 1
        
        while 1:
            # we should attempt to get admin data (uid, token) if it's being refreshed
            if isTokenRefreshThreadActive == 1:
                # wait 500ms
                time.sleep(0.5)
                continue

            user_top_db = "users/" + currentUserUID
            
            admin_tokenId = admin['idToken']
            
            # get LifeFlag flag from database
            prevLifeFlag = db.child(user_top_db + "/LifeFlag").get(admin_tokenId).val()
            
            # toggle the flag
            prevLifeFlag = prevLifeFlag ^ 1

            # update the flag in database (make a change in his life!)
            db.child(user_top_db).update({"LifeFlag" : prevLifeFlag}, admin_tokenId)
            
            # wait some time, give RPi communicator some time to flip/toggle the flag
            time.sleep(1)

            # get LifeFlag flag from database again
            LifeFlag = db.child(user_top_db + "/LifeFlag").get(admin_tokenId).val()

            if LifeFlag == prevLifeFlag: # if no life change happened! (RPi communicator didn't flip/toggle it)
                errorCtr = errorCtr + 1
            else: # RPi communicator was alive
                isUserAlive = 1
                errorCtr = 0

                if isUploadProcessHappening == 0:
                    self.uploadBtnEnableSignal.emit(True)
                    self.browseBtnEnableSignal.emit(True)
                    if isFirstTime == 1:
                        isFirstTime = 0
                        self.statusBarSignal.emit("color: rgb(255, 255, 255); background-color: rgb(0, 100, 0);", u"RPi is alive")
                        
            if errorCtr == 5:
                isUserAlive = 0
                errorCtr = 0

                self.uploadBtnEnableSignal.emit(False)
                self.browseBtnEnableSignal.emit(False)
                self.statusBarSignal.emit("color: rgb(255, 255, 255); background-color: rgb(100, 0, 0);", u"RPi not alive")


    def stop(self):
        self.requestInterruption()
        self.terminate()


class UploaderThread(QtCore.QThread):
    uploadStateSignal = QtCore.Signal(bool)
    statusBarSignal = QtCore.Signal(str, str)
    progressBarSignal = QtCore.Signal(int, int)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        global admin_tokenId
        global user_db_dir
        global currentUserUID
        global file_path

        cloud_file = "users/" + currentUserUID + "/file.elf"

        self.progressBarSignal.emit(50, 100)
        self.statusBarSignal.emit("color: rgb(0, 0, 0); background-color: rgb(255, 255, 0);", u"Uploading...")
        
        # upload file
        storage.child(cloud_file).put(file_path, admin_tokenId)

        # update isNewElf flag in database and set elfProgressMaxRequest to -1 (arbitrary value)
        db.child(user_db_dir).update({"elfProgressMaxRequest" : -1}, admin_tokenId)
        db.child(user_db_dir).update({"isNewElf" : 1}, admin_tokenId)
        
        isNewElf = db.child(user_db_dir + "/isNewElf").get(admin_tokenId).val()

        if isNewElf == 0: #There is an error
            self.progressBarSignal.emit(0, 100)
            self.statusBarSignal.emit("color: rgb(255, 255, 255); background-color: rgb(100, 0, 0);", u"Upload error...")
            #TODO: Add message to complete or cancelling in case of errors
            #value=ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)
        else:
            self.progressBarSignal.emit(100, 100)
            self.statusBarSignal.emit("color: rgb(0, 0, 0); background-color: rgb(0, 255, 0);", u"Upload done")
            #TODO : edit progress to move from 0 to 100
            time.sleep(1)

        self.uploadStateSignal.emit(isNewElf == 1)


    def stop(self):
        self.requestInterruption()
        self.terminate()


app = QApplication(sys.argv)
window = QMainWindow()
Form = Ui_MainWindow()
Form.setupUi(window)
window.show()
sys.exit(app.exec_())

