
import progress
import progress_script
import upload_script



from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import threading , subprocess , time
import sys,os,ntpath,ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import *



file_path = ''
user=''


def progress_script_thread():
    #os.system('progress-script.py')
    if state == 1:
      progress_script.ReadProgress(user)
    else:
      None 

def progress_thread():
    #os.system('progress.py')
    if state == 1:
      progress.ShowProgressBar()
      #self.Status.setText(' Flashing Finished ......')
  
    else:
      None    
    
def Browse_thread():
    global file_path
    root = tk.Tk()
    root.withdraw()
    root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Elf files","*.elf"),("all files")))
    file_path = root.filepath
    


    
    
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
        self.Status = QLineEdit(self.centralwidget)
        self.Status.setObjectName(u"Status")
        self.Status.setGeometry(QRect(120, 240, 271, 31))
        self.Status.setReadOnly(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(18, 239, 81, 31))
        self.label_2.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        

        
        ## we edit here 
        self.Upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)
        
        self.Status.setText(' IDLE ........')
        
        self.setIcon(MainWindow)
        

      

    def setIcon(self,MainWindow):
      appIcon = QIcon("icon.png")
      MainWindow.setWindowIcon(appIcon)
    
    def setIconModes(self,MainWindow):
        icon = QtGui.QPixmap("icon.png")
        label = QtWidgets.QLabel('Sample', MainWindow)
        pixmap = icon.scaled(601, 334, QtCore.Qt.KeepAspectRatio) 
        label.setPixmap(pixmap)    
        label.show()    
        
    def Browse_Handler(self):
      '''
      BrowseThreadHandle = threading.Thread(target=Browse_thread)
      BrowseThreadHandle.start()
      '''
      global file_path
      root = tk.Tk()
      root.withdraw()
      root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ([("Elf files","*.elf")]))
      file_path = root.filepath      


    def Upload_Handler(self):
        global user
        user = self.comboBox.currentIndex()
       
        global state
        #os.system('upload-script.py' + ' ' + str(file_path))   #TODO
        self.Status.setText(' Uploading ....')
        state=upload_script.UploadElfFile(file_path,user)

        
        
        
        if state == 1:    
            #self.Status.setText(' Uploading Finished ....')        
            x=ctypes.windll.user32.MessageBoxW(0, "Done!", "uploading ELf file ", 4)
            print(x)
            
            self.Status.setText(' Flashing ......') 
            
        else:
            self.Status.setText(' Error .....')       
            ctypes.windll.user32.MessageBoxW(0, "Error!", "Failed to upload Elf File ", 0)



        progressScriptThreadHandle = threading.Thread(target=progress_script.ReadProgress(user))
        progressThreadHandle = threading.Thread(target= progress.ShowProgressBar())
        
        #time.sleep(13)
        progressScriptThreadHandle.start()
        
        
        #time.sleep(1)
        progressThreadHandle.start()
        
        
  
        
        
        
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FOTA Project", None))
        self.Browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.Upload_pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"USER_1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"USER_2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"USER_3", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"    USERS", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"  Status", None))
    # retranslateUi


app=QApplication(sys.argv)   #create app and return handeler but it need list of argv
Window=QMainWindow()  # create widget
Form=Ui_MainWindow()  # create form
Form.setupUi(Window)   # to create form inside widget
Window.show()
sys.exit(app.exec_()) 